"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from arch.iw import InstructionWindow, Instruction
from arch.rob import ReorderBuffer
from arch.mem import DataMemory, InstructionsMemory
from datastructures import Programmer

class CPU:
    def __init__(self, mem_size=256, iw_size=10, rob_size=10):
        self.iw = InstructionWindow(iw_size)
        self.rob = ReorderBuffer(rob_size)
        self.dmem = DataMemory(mem_size)
        self.imem = InstructionsMemory()

    def program(self, f):
        programmer = Programmer(self.imem)
        programmer.program(f)