#!/usr/bin/env python
#coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from asm import NOP

class Trap(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class Instruction:
    def __init__(self, codop=NOP, ra=None, rb=None, rc=None):
        self.codop = codop
        self.ra = ra
        self.rb = rb
        self.rc = rc