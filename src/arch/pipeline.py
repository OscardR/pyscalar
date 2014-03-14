#!/usr/bin/env python
# coding:utf8

"""
Created on 08/03/2014
@author: Óscar Gómez Alcañiz <oscar.gomez@uji.es>
"""

from app.log import Log
from datastructures import asm
from datastructures.instruction import Trap

l = Log( "pipeline" )

class Stage:
    """
    Base class for the pipelining implementation
    """
    def __init__( self, name, cpu ):
        self.name = name
        l.v( "Stage %s initialized!" % name, "Stage" )
        self.cpu = cpu

    def prepare( self ):
        raise NotImplementedError( 
            "Stage {0} has not implemented 'prepare' method!".format( self.name ) )

    def execute( self ):
        raise NotImplementedError( 
            "Stage {0} has not implemented 'execute' method!".format( self.name ) )

    def finalize( self ):
        raise NotImplementedError( 
            "Stage {0} has not implemented 'finalize' method!".format( self.name ) )

class IF( Stage ):
    """
    Instruction Fetch
    =================
    Instructions are captured from the instructions memory and inserted onto
    the instructions buffer, at a rate of S instructions per cycle
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "IF", cpu )
        self.S = self.cpu.S

    def prepare( self ):
        self.imem = self.cpu.imem  # Instructions Memory
        self.ib = self.cpu.ib  # Instructions Buffer

    def execute( self ):
        # S-Scalar fetches S instructions per cycle
        for _ in range( self.S ):
            inst = self.imem.get_instruction_at( self.cpu.PC )
            self.ib.insert_instruction( inst )
            self.cpu.increment_PC()

    def finalize( self ):
        pass

class ID( Stage ):
    """
    Instruction Decode
    ==================
    Instructions are inserted onto the instruction window, 
    after fetching the operands from the register bank
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "ID", cpu )

    def prepare( self ):
        self.ib = self.cpu.ib  # Instructions Buffer
        self.iw = self.cpu.iw  # Instructions Window
        self.regs = self.cpu.regs  # Registers Bank
        self.rob = self.cpu.rob # ReOrder Buffer
        self.S = self.cpu.S  # S-Scalar factor

    def execute( self ):
        for _ in range( self.S ):
            inst = self.ib.fetch_instruction()

            if inst == None: continue
            l.d( inst, "ID" )

            ( codop, dest ) = inst.codop, inst.rc
            
            if not self.regs.check_ok(inst.ra):
                op1 = self.rob.get_last(inst.ra)
                ok1 = self.rob.is_ok(op1)
            else:
                op1 = self.regs[inst.ra]
                ok1 = True
            
            if not self.regs.check_ok(inst.ra):
                op2 = self.rob.get_last(inst.rb)
                ok2 = self.rob.is_ok(op2)
            else:
                op2 = self.regs[inst.rb]
                ok2 = True

            type1 = 'INM' if ok1 else 'REG'
            type2 = 'INM' if ok2 else 'REG'

            success = self.iw.insert_instruction( codop, dest, op1, ok1, type1, op2, ok2, type2 )
            if not success:
                pass  # TODO: Somehow set flag to repeat decode next cycle

    def finalize( self ):
        pass

class ISS( Stage ):
    """
    Issue Stage
    ===========
    Instructions which have their operands are issued from the instructions window,
    to their functional units, if they are available for their operation.
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "ISS", cpu )

    def prepare( self ):
        self.S = self.cpu.S
        self.iw = self.cpu.iw
        self.fu = self.cpu.fu

    def execute( self ):
        issued = 0
        n = 0
        while issued < self.S and n < self.iw.size:  # S-scalar processors issue S instructions per cycle
            inst = self.iw.next_ready_instruction()
            if inst == None:  # If no instructions are ready, abort stage
                break
            if inst.codop == asm.TRAP:
                raise Trap( "End of program" )
            elif inst.codop == asm.MUL \
                or inst.codop == asm.MULI \
                or inst.codop == asm.DIV \
                or inst.codop == asm.DIVI:
                if self.fu[asm.MUL].is_available():
                    self.fu[asm.MUL].feed( inst.op1, inst.op2 )
                    issued += 1
            elif inst.codop == asm.ADD \
                or inst.codop == asm.ADDI \
                or inst.codop == asm.SUB \
                or inst.codop == asm.SUBI:
                if self.fu[asm.ADD].is_available():
                    self.fu[asm.ADD].feed( inst.op1, inst.op2 )
                    issued += 1
            n += 1

    def finalize( self ):
        pass

class ALU( Stage ):
    """
    ALU Stage
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "ALU", cpu )

    def prepare( self ):
        self.fu = self.cpu.fu

    def execute( self ):
        for fu in self.fu:
            fu.step()

    def finalize( self ):
        pass

class MEM( Stage ):
    """
    MEM Stage
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "MEM", cpu )

    def prepare( self ):
        self.mem = self.cpu.mem

    def execute( self ):
        for fu in self.fu:
            if fu.is_completed():
                inst = fu.inst
                if inst.codop == asm.SW:
                    self.mem[fu.get_result()] = self.regs[inst.rc]

    def finalize( self ):
        pass

class WB( Stage ):
    """
    WB Stage
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "WB", cpu )

    def prepare( self ):
        self.rob = self.cpu.rob
        self.fu = self.cpu.fu

    def execute( self ):
        for fu in self.fu:
            inst = self.fu.inst
            if inst.codop == asm.LW:
                self.rob[inst.rc] = self.mem[fu.get_result()]

class COM( Stage ):
    """
    COM Stage
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "COM", cpu )
        
    def prepare(self):
        self.regs = self.cpu.regs
        
