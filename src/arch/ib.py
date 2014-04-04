#!/usr/bin/env python
# coding:utf8

"""
Created on 09/03/2014
@author: "Óscar Gómez Alcañiz <oscar.gomez@uji.es>"
"""

from datastructures.instruction import Instruction
import app.log as log
import reg
import datastructures.asm as asm

class InstructionBuffer():
    """
    A circular buffer to store instructions waiting to be decoded
    """
    def __init__( self, n=10 ):
        self.size = n
        self.ins_pos = 0
        self.retr_pos = 0
        self.inst_count = 0
        self.instructions = [None] * self.size

    def push_instruction( self, inst=Instruction() ):
        if self.instructions[self.ins_pos] == None:
            self.instructions[self.ins_pos] = inst
            self._update_ins_pos()
            return True
        else: return False

    def pop_instruction( self ):
        # Get next instruction in the queue
        inst = self.instructions[self.retr_pos]

        # If there are no instructions in the queue, return None
        if inst == None: return None, None

        # Flush that instruction on the buffer
        self.instructions[self.retr_pos] = None
        # Update position
        self._update_retr_pos()
        n_inst = self.inst_count
        self.inst_count += 1
        return n_inst, inst

    def is_empty( self ):
        for inst in self.instructions:
            if inst != None: return False
        return True

    def _update_ins_pos( self ):
        self.ins_pos += 1
        self.ins_pos %= self.size

    def _update_retr_pos( self ):
        self.retr_pos += 1
        self.retr_pos %= self.size

    def __str__( self ):
        out = log.make_title( "InstructionBuffer" )
        for i, inst in enumerate( self.instructions ):
            out += "[ {:>2} ] {:>4} | {} ]\n".format( i, i + self.inst_count, inst )
        return out

if __name__ == '__main__':
    '''
    Test suite
    '''
    ib = InstructionBuffer( 4 )
    ib.push_instruction( Instruction( asm.ADD, reg.r0, reg.r1, reg.r2 ) )
    ib.push_instruction( Instruction( asm.ADDI, reg.r3, reg.r4, reg.r5 ) )
    ib.push_instruction( Instruction( asm.MULT, reg.r6, reg.r7, reg.r8 ) )
    ib.push_instruction( Instruction( asm.MULTI, reg.r9, reg.r10, reg.r11 ) )
    print ib
    for i in range( 6 ):
        print ib.pop_instruction()
    ib.push_instruction( Instruction( asm.MULTI, reg.r9, reg.r10, reg.r11 ) )
    print ib
    for i in range( 6 ):
        print ib.pop_instruction()
