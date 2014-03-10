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
        self.rb = self.cpu.rb  # Registers Bank
        self.S = self.cpu.S  # S-Scalar factor

    def execute( self ):
        for _ in range( self.S ):
            inst = self.ib.fetch_instruction()

            if inst == None: continue
            l.d(inst, "ID")

            ( codop, dest ) = inst.codop, inst.rc

            op1 = self.rb[inst.ra]  # None if not valid
            op2 = self.rb[inst.rb]  # None if not valid

            ok1 = self.rb[op1] != None
            ok2 = self.rb[op2] != None

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

    def execute( self ):
        issued = 0
        while issued < self.S:  # S-scalar processors issue S instructions per cycle
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

    def finalize( self ):
        pass
