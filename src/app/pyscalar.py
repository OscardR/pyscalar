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
import os
import inspect

# Init logging
l = Log( "PyScalar" )

class PyScalar:
    def run( self ):
        l.v( "Iniciando ejecución", "main" )

        # Create CPU
        cpu = CPU()

        # Create Programmer
        prog = Programmer( cpu.imem )

        # Load program in Instruction Memory
        prog.program( os.path.dirname( os.path.abspath( inspect.getfile( inspect.currentframe() ) ) ) + '/code.asm' )

        # Start CPU
        cpu.run()

        # Debug architecture status
        print cpu.imem
        print cpu.dmem
        print cpu.ib
        print cpu.iw
        print cpu.regs
        print cpu.rob
        for unit in cpu.fu:
            print cpu.fu[unit]

        l.v( "Fin de la ejecución", "main" )
