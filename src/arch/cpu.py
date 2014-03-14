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
from pipeline import IF, ID, ISS
import reg
import fu
from app.log import Log
from datastructures import asm
from datastructures.instruction import Trap

l = Log( "CPU" )

class CPU:
    def __init__( self, mem_size=256, iw_size=10, rob_size=10, N=8, S=2 ):
        # Initialize architecture
        self.rob = ReorderBuffer( rob_size )
        self.dmem = DataMemory( mem_size )
        self.imem = InstructionsMemory()
        self.ib = InstructionBuffer()
        self.iw = InstructionWindow( iw_size )
        self.regs = Registers()
        self.fu = [FunctionalUnit( fu.MULT ), FunctionalUnit( fu.SUM )]
        self.PC = 0x00
        self.N = N
        self.S = S

        # Initialize stages
        if_st = IF( self )
        id_st = ID( self )
        iss_st = ISS( self )
        """
        exe_st = EXE(self)
        os_st = OS(self)
        com_st = COM(self)
        """
        self.stages = [if_st, id_st, iss_st]  # , exe_st, os_st, com_st ]

    def run( self ):
        # Loop through instructions, then through stages in reverse
        while True:
            try:
                for stage in reversed( self.stages ):
                    stage.prepare()
                    stage.execute()
                    stage.finalize()
            except Trap:
                break

    def increment_PC( self ):
        self.PC += 1

if __name__ == '__main__':
    l.v( "Test Init", "main" )
    cpu = CPU()
    l.d( cpu.regs, "Registers" )
    l.d( cpu.imem, "InstructionMemory" )
    l.d( cpu.dmem, "DataMemory" )
    l.v( "Test End", "main" )
