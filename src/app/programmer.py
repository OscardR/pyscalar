#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from datastructures.instruction import Instruction
from datastructures import asm
from arch import reg
from app.log import Log
import re

l = Log( "programmer" )

class Programmer:
    """
    Helper class to read assembler code from a file and insert the instructions
    to the instructions memory
    """

    def __init__( self, memory ):
        self.memory = memory

    def program( self, code ):
        for line in open( code ):
            self.insert_instruction( line )

    def insert_instruction( self, instruction_line ):
        try:
            # Arithmetical instructions
            codop, dest, op1, op2 = re.split( ',? ', instruction_line.strip() )
        except ValueError:
            try:
                # Memory access instructions
                codop, dest, op2, op1 = re.split( ',? |\(', re.sub( '\)', '', instruction_line.strip() ) )
            except ValueError:
                # NOP & TRAP instructions
                codop, dest, op1, op2 = instruction_line.strip(), None, None, None

        # Find values for opcode and regs
        codop = asm.__dict__[codop.upper()]

        # If operation code is not a TRAP...
        if codop != asm.TRAP:

            # ...get destination register
            dest = reg.__dict__[dest.lower()]

            # If operation code is not for immediate values calculation...
            if codop not in [asm.ADDI, asm.MULTI, asm.SUBI, asm.LW, asm.SW]:

                # ...get 2nd operator
                op2 = reg.__dict__[op2.lower()]

            # Get 1st operator
            op1 = reg.__dict__[op1.lower()]

        # Create instruction...
        inst = Instruction( codop, dest, op1, op2 )

        # ...and insert in memory
        self.memory.insert_instruction( inst )

        l.d( "[ {} ] >> IMEM".format( inst ), "insert_instruction" )
