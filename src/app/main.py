#!/usr/bin/env python
#coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""
from arch.cpu import CPU
from programmer import Programmer
from log import Log

if __name__ == '__main__':
    l = Log('PyScalar')
    l.v("Iniciando ejecución", "main")
    cpu = CPU()
    prog = Programmer(cpu.imem)
    prog.program('code.asm')
    cpu.run()
    l.v("Fin de la ejecución", "main")