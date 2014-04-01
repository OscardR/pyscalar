#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from datastructures import asm
from datastructures.instruction import Instruction
import app.log as log

class InstructionWindowLine:
    def __init__( self, codop=asm.NOP, dest=None, op1=None, ok1=False, op2=None, ok2=False ):
        self.codop = codop
        self.dest = dest
        self.op1 = op1
        self.ok1 = ok1
        self.op2 = op2
        self.ok2 = ok2

    def __str__( self ):
        return "{:>6} | {:>4} | {:>4} | {:>3} | {:>4} | {:>3}".format( 
            self.codop,
            self.dest if self.dest != None else '—',
            self.op1 if self.op1 != None else '—',
            self.ok1,
            self.op2 if self.op2 != None else '—',
            self.ok2 )

class InstructionWindow:
    def __init__( self, n=10 ):
        self.size = n
        self.lines = [None] * self.size

    def insert_instruction( self, codop=asm.NOP, dest=None, op1=None, ok1=False, op2=None, ok2=False ):
        # Find a free slot
        for pos in range( len( self.lines ) ):
            if self.lines[pos] == None:
                self.lines[pos] = InstructionWindowLine( codop, dest, op1, ok1, op2, ok2 )
                return True
        # Couldn't insert instruction, window full
        return False

    def next_ready_instruction( self ):
        # Find an instruction ready to be issued
        for pos, inst_line in enumerate( self.lines ):
            if inst_line != None and inst_line.ok1 and inst_line.ok2:
                return pos, Instruction( inst_line.codop, inst_line.dest, inst_line.op1, inst_line.op2 )
        return None, None

    def flush( self, pos ):
        self.lines[pos] = None

    def __str__( self ):
        out = log.make_title( "InstructionWindow" )
        out += "[ {:>6} | {:>4} | {:>4} | {:>3} | {:>4} | {:>3} ]\n"\
            .format( "codop", "dest", "op1", "ok1", "op2", "ok2" )
        out += "[{:>6}|{:>4}|{:>4}|{:>3}|{:>4}|{:>3}]\n"\
            .format( "--------", "------", "------", "-----", "------", "-----" )
        for il in self.lines:
            if il != None:
                out += "[ {} ]\n".format( str( il ) )
        return out

if __name__ == '__main__':
    iwl = InstructionWindowLine()
    print iwl
