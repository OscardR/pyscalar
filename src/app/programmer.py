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

l = Log( "Programmer" )

class Programmer:
    def __init__( self, memory ):
        self.memory = memory

    def program( self, code ):
        for line in open( code ):
            self.insert_instruction( line )

    def insert_instruction( self, instruction_line ):
        try:
            # Instrucciones aritméticas
            op, rc, ra, rb = re.split( ',? ', instruction_line.strip() )
        except ValueError:
            try:
                # Instrucciones de memoria
                op, rc, rb, ra = re.split( ',? |\(', re.sub( '\)', '', instruction_line.strip() ) )
            except ValueError:
                # Instrucciones NOP y TRAP
                op, rc, ra, rb = instruction_line.strip(), None, None, None
        # Find values for opcode and regs
        op = asm.__dict__[op.upper()]
        if op != asm.TRAP:
            rc = reg.__dict__[rc.lower()]
            if op not in [asm.ADDI, asm.MULI, asm.SUBI]:
                rb = reg.__dict__[rb.lower()]
            ra = reg.__dict__[ra.lower()]
        # Create instruction and insert in memory
        inst = Instruction( op, ra, rb, rc )
        self.memory.insert_instruction( inst )
        l.d( "Insert: {inst}".format( **locals() ), "Programmer" )
