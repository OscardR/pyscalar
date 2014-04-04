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
import app.defaults as DEF

from app.log import Log
from datastructures import asm
from datastructures.instruction import Trap

l = Log( "cpu" )
STEP_BY_STEP = True

class CPU:
    def __init__( self, mem_size=DEF.MEM_SIZE, iw_size=DEF.IW_SIZE, rob_size=DEF.ROB_SIZE, S=DEF.S ):
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

        # CPU parameters: S -> Scalarity factor 
        # (Instructions fetched/decoded per cycle)
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

        # Cycles count
        self.cycle = 0

        # Control flag
        self.running = True

        # Loop through instructions, then through stages in reverse
        while self.running:
            try:
                # Log cycle #
                l.v( self.cycle, "Cycle" )

                # Iterate stages, from last to first
                for stage in reversed( self.stages ):

                    # Execute stage...
                    try:
                        stage.execute()
                    # ...capturing TRAP
                    except Trap as trap_ex:

                        # Log trap
                        l.e( trap_ex, "Trap" )

                        # Increment trap count
                        self.trap_count += 1

                # Check whether all stages have propagated trap...
                if self.trap_count >= len( self.stages ) - 1:

                    # ...and then make sure pipeline is finished
                    if self.ib.is_empty() \
                        and self.rob.is_empty() \
                        and self.iw.is_empty():

                        # then finish execution
                        self.finish()

            # Check for keyboard interruption every cycle...
            except KeyboardInterrupt as kb_int:

                # ...log it...
                l.e( kb_int )

                # ...then cancel execution
                self.finish( cancelled=True )

            # Always increment cycle and check for step by step flag
            finally:
                self.cycle += 1
                try:
                    # If execution step by step is set, wait for key...
                    if STEP_BY_STEP:
                        raw_input()
                # ...and stop execution on Ctrl+C
                except KeyboardInterrupt:
                    self.finish( cancelled=True )

    def finish( self, cancelled=False ):
        if cancelled:
            l.e( "Execution ABORTED", "finish" )
        else:
            l.v( "Execution FINISHED", "finish" )
        self.running = False

    def has_trapped( self ):
        return self.trap_count > 0

    def increment_PC( self ):
        l.v( self.PC, "PC" )
        self.PC += 1

if __name__ == '__main__':
    l.v( "Test Init", "CPU" )
    cpu = CPU()
    l.d( cpu.imem, "InstructionMemory" )
    l.d( cpu.ib, "InstructionBuffer" )
    l.d( cpu.iw, "InstructionWindow" )
    l.d( cpu.rob, "ReorderBuffer" )
    l.d( cpu.dmem, "DataMemory" )
    l.d( cpu.regs, "Registers" )
    l.v( "Test End", "CPU" )
