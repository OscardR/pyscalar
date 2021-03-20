#!/usr/bin/env python
# coding:utf8

"""
Created on 03/04/2014
@author: "Óscar Gómez Alcañiz <oscar.gomez@uji.es>"
"""

# App imports
from arch.cpu import CPU
from .programmer import Programmer
from .log import Log
from .defaults import DEF

import os
import sys
import inspect

# Init logging
L = Log("pyscalar")


class PyScalar:
    def __init__(
        self,
        code=DEF.ASM_CODE,
        mem_size=DEF.MEM_SIZE,
        iw_size=DEF.IW_SIZE,
        rob_size=DEF.ROB_SIZE,
        S=DEF.S,
    ):
        self.code = code
        self.mem_size = mem_size
        self.iw_size = iw_size
        self.rob_size = rob_size
        self.S = S

    def start(self):
        L.v("Iniciando ejecución", "run")

        # Create CPU
        self.cpu = CPU(
            mem_size=self.mem_size,
            iw_size=self.iw_size,
            rob_size=self.rob_size,
            S=self.S,
        )

        # Create Programmer
        self.prog = Programmer(self.cpu.imem)

        # Load program in Instruction Memory
        self.prog.program(
            os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            + "/"
            + self.code
        )

        # Start CPU
        self.cpu.start()

    def run(self):
        self.start()
        self.cpu.run()
        self.finish()

    def finish(self):
        # Print architecture status
        L.v(self.cpu.imem, "run")
        L.v(self.cpu.dmem, "run")
        L.v(self.cpu.ib, "run")
        L.v(self.cpu.iw, "run")
        L.v(self.cpu.regs, "run")
        L.v(self.cpu.rob, "run")
        for unit in self.cpu.fu:
            L.v(self.cpu.fu[unit], "run")

        L.v("Fin de la ejecución", "run")

    def step(self, steps=1):
        self.cpu.step(steps)


if __name__ == "__main__":

    # Code to load and execute
    asm_code = DEF.ASM_CODE

    # Scalarity factor
    s = DEF.S

    num_args = len(sys.argv)
    if num_args >= 2:
        asm_code = sys.argv[1]
        if num_args > 2:
            s = int(sys.argv[2])

    # Init PyScalar Sim with current parameters
    pyscalar = PyScalar(code=asm_code, S=s)
    app.run()
