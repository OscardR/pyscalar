#!/usr/bin/env python
#coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez Alcañiz <oscar.gomez@uji.es>
"""
import app.log
from app.log import Log
from datastructures.instruction import Instruction

class InstructionsMemory:
    def __init__(self):
        self.instructions = []

    def insert_instruction(self, instruction):
        self.instructions.append(instruction)

    def get_instruction_at(self, pc):
        try:
            return self.instructions[pc]
        except IndexError:
            return Instruction()
            #raise EndOfProgram("No more instructions.")

l = Log("DataMemory")        
class DataMemory:
    def __init__(self, size=32):
        self.memory = [word for word in xrange(size)]

    def read_byte(self, index):
        l.d("Read: {}".format(index), "Memory")
        return self.memory[index]

    def write_byte(self, index, data):
        l.d("Write: {} <= {}".format(index, data), "Memory")
        self.memory[index] = data

    def __str__(self):
        out = "{}Memory:{}\n".format(app.log.RED_BOLD, app.log.NORMAL)
        for i, w in enumerate(self.memory):
            out += "[ {:#04x} ] ".format(w)
            if i % 8 == 7: out += "\n"
        return out