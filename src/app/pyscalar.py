#!/usr/bin/env python
# coding:utf8

"""
Created on 03/04/2014
@author: "Óscar Gómez Alcañiz <oscar.gomez@uji.es>"
"""

# App imports
from arch.cpu import CPU
from programmer import Programmer
from log import Log
import defaults as DEF

import os
import sys
import inspect

# Init logging
l = Log( "pyscalar" )

class PyScalar:
    def __init__( self, code=DEF.ASM_CODE, mem_size=DEF.MEM_SIZE, iw_size=DEF.IW_SIZE, rob_size=DEF.ROB_SIZE, S=DEF.ROB_SIZE ):
        self.code = code
        self.mem_size = mem_size
        self.iw_size = iw_size
        self.rob_size = rob_size
        self.S = S

    def run( self ):
        l.v( "Iniciando ejecución", "run" )

        # Create CPU
        cpu = CPU( mem_size=self.mem_size, iw_size=self.iw_size, rob_size=self.rob_size, S=self.S )

        # Create Programmer
        prog = Programmer( cpu.imem )

        # Load program in Instruction Memory
        prog.program( os.path.dirname( os.path.abspath( inspect.getfile( inspect.currentframe() ) ) ) + '/' + self.code )

        # Start CPU
        cpu.run()

        # Print architecture status
        l.v( cpu.imem, "run" )
        l.v( cpu.dmem, "run" )
        l.v( cpu.ib, "run" )
        l.v( cpu.iw, "run" )
        l.v( cpu.regs, "run" )
        l.v( cpu.rob, "run" )
        for unit in cpu.fu:
            l.v( cpu.fu[unit], "run" )

        l.v( "Fin de la ejecución", "run" )

if __name__ == '__main__':

    # Code to load and execute
    asm_code = DEF.ASM_CODE

    # Scalarity factor
    s = DEF.S

    num_args = len( sys.argv )
    if num_args >= 2:
        asm_code = sys.argv[1]
        if num_args > 2:
            s = int( sys.argv[2] )

    # Init PyScalar Sim with current parameters
    pyscalar = PyScalar( code=asm_code, S=s )
    pyscalar.run()
