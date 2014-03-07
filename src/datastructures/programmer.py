"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from instruction import Instruction
from app.log import Log
import re

l = Log("Programmer")

class Programmer:
    def __init__(self, memory):
        self.memory = memory
        
    def program(self, code):
        for line in open(code):
            self.insert_instruction(line)

    def insert_instruction(self, instruction_line):
        try:
            # Instrucciones aritméticas
            op, rc, ra, rb = re.split(',? ', instruction_line.strip())
        except ValueError:
            try:
                # Instrucciones de memoria
                op, rc, rb, ra = re.split(',? |\(', re.sub('\)', '', instruction_line.strip()))
            except ValueError:
                # Instrucciones NOP y TRAP
                op, rc, ra, rb = instruction_line.strip(), None, None, None
        ins = Instruction(op, ra, rb, rc)
        self.memory.insert_instruction(ins)
        l.d("Insert: {ins}".format(**locals()), "Programmer")