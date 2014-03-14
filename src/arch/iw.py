#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from datastructures import asm
from datastructures.instruction import Instruction

class InstructionWindowLine:
    def __init__( self, codop=asm.NOP, dest=None, op1=None, ok1=False, type1=None, op2=None, ok2=False, type2=None ):
        self.codop = codop
        self.dest = dest
        self.op1 = op1
        self.ok1 = ok1
        self.type1 = type1
        self.op2 = op2
        self.ok2 = ok2
        self.type2 = type2

    def __str__( self ):
        return "[ {:>6} | {:>4} | {:>4} | {:>1} | {:>4} | {:>1} ]".format( 
            self.codop,
            self.dest if self.dest != None else '—',
            self.op1 if self.op1 != None else '—',
            self.ok1,
            self.op2 if self.op2 != None else '—',
            self.ok2 )

class InstructionWindow:
    def __init__( self, n=10 ):
        self.size = n
        self.instructions = [None] * self.size

    def insert_instruction( self, codop=asm.NOP, dest=None, op1=None, ok1=False, type1=None, op2=None, ok2=False, type2=None ):
        for pos in range( len( self.instructions ) ):
            if self.instructions[pos] == None:
                self.instructions[pos] = InstructionWindowLine( codop, dest, op1, ok1, type1, op2, ok2, type2 )
                return True
        # Couldn't insert instruction, window full
        return False

    def next_ready_instruction( self ):
        for pos in range( len( self.instructions ) ):
            inst_line = self.instructions[pos]
            if inst_line != None and inst_line.ok1 and inst_line.ok2:
                return Instruction( inst_line.codop, inst_line.dest, inst_line.op1, inst_line.op2 )
        return None

if __name__ == '__main__':
    iwl = InstructionWindowLine()
    print iwl
