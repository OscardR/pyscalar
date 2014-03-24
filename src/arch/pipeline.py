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

    def execute( self ):
        raise NotImplementedError( 
            "Stage {0} has not implemented 'execute' method!".format( self.name ) )


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
        self.imem = self.cpu.imem  # Instructions Memory
        self.ib = self.cpu.ib  # Instructions Buffer

    def execute( self ):
        # S-Scalar fetches S instructions per cycle
        for _ in range( self.S ):
            inst = self.imem.get_instruction_at( self.cpu.PC )
            self.ib.insert_instruction( inst )
            self.cpu.increment_PC()

class ID( Stage ):
    """
    Instruction Decode
    ==================
    Instructions are inserted onto the instruction window, 
    after fetching the operands from the register bank
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "ID", cpu )
        self.ib = self.cpu.ib  # Instructions Buffer
        self.iw = self.cpu.iw  # Instructions Window
        self.regs = self.cpu.regs  # Registers Bank
        self.rob = self.cpu.rob  # ReOrder Buffer
        self.S = self.cpu.S  # S-Scalar factor

    def execute( self ):
        for _ in range( self.S ):
            inst = self.ib.fetch_instruction()

            if inst == None: continue
            l.d( inst, "ID" )

            ( codop, dest ) = inst.codop, inst.rc

            # TODO: Change logic in order to use ROB to read register values
            if codop not in [asm.TRAP, asm.NOP]:
                regs = [dest, inst.ra]
                if codop not in [asm.MULI, asm.ADDI, asm.DIVI, asm.SUBI]:
                    regs.append( inst.rb )

                for reg in regs:
                    self.rob.insert_line( dest=reg, value=self.regs[reg], ok=self.regs.check_ok( reg ) )

                op1 = self.rob.get_last_index( inst.ra )
                ok1 = self.rob[ op1 ].ok

                if codop not in [asm.MULI, asm.ADDI, asm.DIVI, asm.SUBI]:
                    op2 = self.rob.get_last_index( inst.rb )
                    ok2 = self.rob[ op2 ].ok

                type1 = 'INM' if ok1 else 'REG'
                type2 = 'INM' if ok2 else 'REG'

                success = self.iw.insert_instruction( codop, dest, op1, ok1, type1, op2, ok2, type2 )
                if not success:
                    pass  # TODO: Somehow set flag to repeat decode next cycle
            else:  # TODO: Do something about TRAP instructions
                if codop == asm.TRAP:
                    raise Trap()

class ISS( Stage ):
    """
    Issue Stage
    ===========
    Instructions which have their operands are issued from the instructions window,
    to their functional units, if they are available for their operation.
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "ISS", cpu )
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
                    self.fu[asm.ADD].feed( inst.ra, inst.rb )
                    issued += 1
            n += 1

class ALU( Stage ):
    """
    ALU Stage
    =========
    In this stage all functional units compute a cycle.
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "ALU", cpu )
        self.fu = self.cpu.fu

    def execute( self ):
        for t in self.fu:
            fu = self.fu[t]
            fu.step()

class MEM( Stage ):
    """
    MEM Stage
    =========
    In this stage results from completed functional 
    units are written to memory. 
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "MEM", cpu )
        self.mem = self.cpu.dmem
        self.fu = self.cpu.fu

    def execute( self ):
        for t in self.fu:
            fu = self.fu[t]
            if fu.is_completed():
                if fu.op == asm.SW:
                    self.mem[fu.get_result()] = self.regs[fu.dest]

class WB( Stage ):
    """
    WB Stage
    ========
    In this stage all results from finished functional units 
    are written to the reorder buffer.
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "WB", cpu )
        self.rob = self.cpu.rob
        self.fu = self.cpu.fu

    def execute( self ):
        for t in self.fu:
            fu = self.fu[t]
            if fu.is_completed():
                if fu.op == asm.LW:
                    i = self.rob.get_last_index[fu.dest]
                    self.rob[i].set_value( self.mem[fu.get_result()] )

class COM( Stage ):
    """
    COM Stage
    =========
    In this stage all correct values from the reorder buffer get written 
    to their correspondent registers in the register bank.
    """
    def __init__( self, cpu ):
        Stage.__init__( self, "COM", cpu )
        self.regs = self.cpu.regs
        self.rob = self.cpu.rob

    def execute( self ):
        for line in self.rob.lines:
            if line != None and line.ok:
                self.regs[line.dest] = line.value
