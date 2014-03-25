#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

NOP = 'nop'
ADD = 'add'
SUB = 'sub'
MUL = 'mult'
DIV = 'div'
ADDI = 'addi'
SUBI = 'subi'
MULI = 'multi'
DIVI = 'divi'
AND = 'and'
OR = 'or'
XOR = 'xor'
NAND = 'nand'
TRAP = 'trap'
LW = 'lw'
SW = 'sw'

def name( codop ):
    l = None
    for l in globals():
        if globals()[l] == codop and l != 'codop': return l
    return "{}".format( codop )
