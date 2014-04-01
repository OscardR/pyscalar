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
    def __init__( self, n=10 ):
        self.size = n
        self.ins_pos = 0
        self.retr_pos = 0
        self.instructions = [None] * self.size

    def queue_instruction( self, inst=Instruction() ):
        if self.instructions[self.ins_pos] == None:
            self.instructions[self.ins_pos] = inst
            self._update_ins_pos()
            return True
        else: return False

    def fetch_instruction( self ):
        inst = self.instructions[self.retr_pos]
        return inst

    def flush_instruction( self ):
        self.instructions[self.retr_pos] = None
        self._update_retr_pos()

    def _update_ins_pos( self ):
        self.ins_pos += 1
        if self.ins_pos >= self.size:
            self.ins_pos = 0

    def _update_retr_pos( self ):
        self.retr_pos += 1
        if self.retr_pos >= self.size:
            self.retr_pos = 0

    def __str__( self ):
        out = log.make_title( "InstructionBuffer" )
        for i, inst in enumerate( self.instructions ):
            out += "[ {:>2} | {} ]\n".format( i, inst )
        return out

if __name__ == '__main__':
    '''
    Test suite
    '''
    ib = InstructionBuffer( 4 )
    ib.queue_instruction( Instruction( asm.ADD, reg.r0, reg.r1, reg.r2 ) )
    ib.queue_instruction( Instruction( asm.ADDI, reg.r3, reg.r4, reg.r5 ) )
    ib.queue_instruction( Instruction( asm.MUL, reg.r6, reg.r7, reg.r8 ) )
    ib.queue_instruction( Instruction( asm.MULI, reg.r9, reg.r10, reg.r11 ) )
    print ib
    for i in range( 6 ):
        print ib.fetch_instruction()
