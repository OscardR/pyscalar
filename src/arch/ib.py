#!/usr/bin/env python
#coding:utf8

"""
Created on 09/03/2014
@author: "Óscar Gómez Alcañiz <oscar.gomez@uji.es>"
"""

from datastructures.instruction import Instruction

class InstructionBuffer():
    def __init__(self, n=10):
        self.size = n
        self.pos = 0
        self.instructions = [None] * self.size
        
    def insert_instruction(self, inst=Instruction()):
        self.instructions[self.pos] = inst
        self._update_pos()
        return self.pos
    
    def fetch_instruction(self):
        inst = self.instructions[self.pos]
        self._update_pos()
        return inst 
    
    def _update_pos(self):
        self.pos = self.pos + 1
        if self.pos >= self.size:
            self.pos = 0
        