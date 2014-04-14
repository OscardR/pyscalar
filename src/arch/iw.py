#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from datastructures import asm
from datastructures.instruction import Instruction
from arch import reg
import app.log as log

class InstructionWindowLine:
    def __init__( self, n_inst, codop=asm.NOP, dest=None, op1=None, ok1=False, op2=None, ok2=False ):
        self.n_inst = n_inst
        self.codop = codop
        self.dest = dest
        self.dest_name = reg.name( self.dest )
        self.op1 = op1
        self.ok1 = ok1
        self.op2 = op2
        self.ok2 = ok2

    def __str__( self ):
        return "I{:<4} | {:>6} | {:>4} | {:>4} | {:>3} | {:>4} | {:>3}".format( 
            self.n_inst,
            self.codop,
            self.dest if self.dest != None else "-",
            self.op1 if self.op1 != None else "-",
            self.ok1,
            self.op2 if self.op2 != None else "-",
            self.ok2 )

class InstructionWindow:
    def __init__( self, n=10 ):
        self.size = n
        self.full = False
        self.lines = [None] * self.size

    def insert_instruction( self, n_inst, codop=asm.NOP, dest=None, op1=None, ok1=False, op2=None, ok2=False ):
        # Find a free slot
        for pos in range( len( self.lines ) ):
            if self.lines[pos] == None:
                self.lines[pos] = InstructionWindowLine( n_inst, codop, dest, op1, ok1, op2, ok2 )
                return True
        # Couldn't insert instruction, window full
        return False

    def next_ready_instruction( self ):
        # Find an instruction ready to be issued
        for pos, inst_line in enumerate( self.lines ):
            if inst_line != None and \
                ( ( inst_line.ok1 and inst_line.ok2 ) or \
                  inst_line.codop == asm.TRAP ):
                return pos, inst_line.n_inst, Instruction( inst_line.codop, inst_line.dest, inst_line.op1, inst_line.op2 )
        return None, None, None

    def get_blocked_instructions( self, rob_index ):
        inst_lines = []
        for inst_line in self.lines:
            if inst_line != None \
                and ( inst_line.op1 == rob_index and not inst_line.ok1\
                or inst_line.op2 == rob_index and not inst_line.ok2 ):
                inst_lines.append( inst_line )
        return inst_lines

    def is_full( self ):
        return None not in self.lines

    def is_empty( self ):
        for inst_line in self.lines:
            if inst_line != None: return False
        return True

    def flush_instruction( self, pos ):
        self.lines[pos] = None

    def __str__( self ):
        out = log.make_title( "InstructionWindow" )
        out += "        [ {:>6} | {:>4} | {:>4} | {:>3} | {:>4} | {:>3} ]\n"\
            .format( "codop", "dest", "op1", "ok1", "op2", "ok2" )
        out += "        [{:>6}|{:>4}|{:>4}|{:>3}|{:>4}|{:>3}]\n"\
            .format( "--------", "------", "------", "-----", "------", "-----" )
        for il in self.lines:
            if il != None:
                out += "[ {} ]\n".format( str( il ) )
        return out

if __name__ == '__main__':
    iwl = InstructionWindowLine( 1 )
    print iwl
