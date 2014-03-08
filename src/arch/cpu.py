"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from iw import InstructionWindow
from rob import ReorderBuffer
from mem import DataMemory, InstructionsMemory

class CPU:
    def __init__(self, mem_size=256, iw_size=10, rob_size=10):
        self.iw = InstructionWindow(iw_size)
        self.rob = ReorderBuffer(rob_size)
        self.dmem = DataMemory(mem_size)
        self.imem = InstructionsMemory()
        self.PC = 0x00
        
    def run(self):
        # Initialize stages
        # Loop through instructions, then through stages, in reverse
        pass