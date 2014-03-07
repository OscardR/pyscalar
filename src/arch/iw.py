"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from datastructures.instruction import Instruction

class InstructionWindow:
    def __init__(self, n=10):
        self.size = n
        self.pos = 0
        self.instructions = [None] * self.size
        
    def insert_instruction(self, ins=Instruction()):
        self.instructions[self.pos] = ins
        self.pos = self.pos + 1
        if self.pos >= self.size:
            self.pos = 0
        return self.pos