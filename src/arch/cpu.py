#!/usr/bin/env python
#coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from iw import InstructionWindow
# from rob import ReorderBuffer
from mem import DataMemory, InstructionsMemory
from arch.reg import Registers
from arch.pipeline import IF, ID
from arch import reg
from app.log import Log
from datastructures import asm

l = Log("CPU")

class CPU:
    def __init__(self, mem_size=256, iw_size=10, rob_size=10, N=8, S=2):
        self.iw = InstructionWindow(iw_size)
        # self.rob = ReorderBuffer(rob_size)
        self.dmem = DataMemory(mem_size)
        self.imem = InstructionsMemory()
        self.regs = Registers()
        self.PC = 0x00
        self.N = N
        self.S = S
        
    def run(self):
        # Initialize decoupling registers
        if_id = {
            'CODOP' : asm.NOP,
            'Ra' : reg.zero,
            'Rb' : reg.zero,
            'Rc' : reg.zero
            }
        id_iss = if_id.copy()
        id_iss.update({
            'A' : 0x00,
            'B' : 0x00,
            'C' : 0x00
            })
        # Initialize stages
        if_st = IF(self, if_id)
        id_st = ID(if_id, id_iss)
        # Loop through instructions, then through stages, in reverse
        pass
    
    def increment_PC(self):
        self.PC += 1
    
if __name__ == '__main__':
    l.v("Test Init", "main")
    cpu = CPU()
    l.d(cpu.regs, "Registers")
    l.d(cpu.imem, "InstructionMemory")
    l.d(cpu.dmem, "DataMemory")
    l.v("Test End", "main")
    