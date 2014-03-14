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
        self.regs = rb
        self.rc = rc
    
    def __repr__(self):
        op = self.codop
        ra = self.ra
        rb = self.regs
        rc = self.rc
        return "Instruction({}, {}, {}, {})".format(op, rc, ra, rb)
        
    def __str__(self):
        op = self.codop
        ra = self.ra if self.ra else u'\u2014'
        rb = self.regs if self.regs else u'\u2014'
        rc = self.rc if self.rc else u'\u2014'
        return u"{} {} {} {}".format(op, rc, ra, rb).encode('utf-8')