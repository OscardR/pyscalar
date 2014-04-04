#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from iw import InstructionWindow
from ib import InstructionBuffer
from rob import ReorderBuffer
from mem import DataMemory, InstructionsMemory
from reg import Registers
from fu import FunctionalUnit
from pipeline import IF, ID, ISS, ALU, MEM, WB, COM

from app.log import Log
from datastructures import asm
from datastructures.instruction import Trap

l = Log( "CPU" )
STEP_BY_STEP = False

class CPU:
    def __init__( self, mem_size=256, iw_size=10, rob_size=10, N=8, S=2 ):
        # Initialize architecture
        self.rob = ReorderBuffer( rob_size )
        self.dmem = DataMemory( mem_size )
        self.imem = InstructionsMemory()
        self.ib = InstructionBuffer()
        self.iw = InstructionWindow( iw_size )
        self.regs = Registers()
        self.fu = {
            asm.MULT : FunctionalUnit( asm.MULT ),
            asm.ADD : FunctionalUnit( asm.ADD ) }
        self.PC = 0x00

        # CPU parameters
        self.N = N
        self.S = S

        # Initialize stages
        if_st = IF( self )
        id_st = ID( self )
        iss_st = ISS( self )
        alu_st = ALU( self )
        mem_st = MEM( self )
        wb_st = WB( self )
        com_st = COM( self )

        self.stages = [if_st, id_st, iss_st, alu_st, mem_st, wb_st, com_st ]

    def run( self ):
        # Initialize the Trap count, to stop when every stage has raised Trap
        self.trap_count = 0
        self.cycle = 0

        # Loop through instructions, then through stages in reverse
        while True:
            try:
                l.v( self.cycle, "Cycle" )
                for stage in reversed( self.stages ):
                    try:
                        stage.execute()
                    except Trap as trap_ex:
                        l.e( trap_ex, "Trap" )
                        self.trap_count += 1
                if self.trap_count >= len( self.stages ) - 1:
                    if self.ib.is_empty() \
                        and self.rob.is_empty() \
                        and self.iw.is_empty():
                        break
            except KeyboardInterrupt as kb_int:
                l.e( kb_int )
                break
            finally:
                self.cycle += 1
                try:
                    if STEP_BY_STEP:
                        raw_input()
                except KeyboardInterrupt:
                    break

    def has_trapped( self ):
        return self.trap_count > 0

    def increment_PC( self ):
        l.v( self.PC, "PC" )
        self.PC += 1

if __name__ == '__main__':
    l.v( "Test Init", "CPU" )
    cpu = CPU()
    l.d( cpu.regs, "Registers" )
    l.d( cpu.imem, "InstructionMemory" )
    l.d( cpu.dmem, "DataMemory" )
    l.v( "Test End", "CPU" )
