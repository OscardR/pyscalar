#!/usr/bin/env python
#coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from datastructures.instruction import Instruction

class InstructionWindowLine():
    def __init__(self, ins=Instruction(), ok1=False, ok2=False):
        self.ins = ins
        self.ok1 = ok1
        self.ok2 = ok2
        
class InstructionWindow:
    def __init__(self, n=10):
        self.size = n
        self.instructions = [None] * self.size
        
    def insert_instruction(self, ins=Instruction()):
        for pos in range(len(self.instructions)):
            if self.instructions[pos] == None:
                self.instructions[pos] = InstructionWindowLine(ins, ok1=False, ok2=False)
                return True
        # Couldn't insert instruction, window full
        return False
    
    def fetch_instruction(self, pos):
        insl = self.instructions[pos]
        self.instructions[pos] = None
        return insl.ins
    
    def next_ready_instruction(self):
        for pos in range(len(self.instructions)):
            insl = self.instructions[pos]
            if insl != None and insl.ok1 and insl.ok2:
                return insl.ins