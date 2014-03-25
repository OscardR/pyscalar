#!/usr/bin/env python
# coding:utf8

"""
Created on 14/03/2014
@author: "Óscar Gómez Alcañiz <oscar.gomez@uji.es>"
"""

from datastructures import asm

class FunctionalUnit():
    """
    Functional Unit
    ===============
    Computes operations
    """

    def __init__( self, op=asm.ADD, cycles=1 ):
        self.op = op
        self.op1 = None
        self.op2 = None
        self.available = True
        self.completed = False
        self.result = None
        self.cycles = cycles
        self.countdown = cycles

    def feed( self, op1, op2 ):
        if self.available:
            self.op1 = op1
            self.op2 = op2
            self.countdown = self.cycles
            self.available = False

    def step( self ):
        if self.op1 != None and \
            self.op2 != None:
            self.countdown -= 1
            if self.countdown == 0:
                if self.op == asm.MUL:
                    self.result = self.op1 * self.op2
                elif self.op == asm.ADD:
                    self.result = self.op1 + self.op2
                elif self.op == asm.SUB:
                    self.result = self.op1 - self.op2
                elif self.op == asm.DIV:
                    self.result = self.op1 / self.op2
                self.completed = True
        return self.countdown

    def is_available( self ):
        return self.available

    def is_completed( self ):
        return self.completed

    def get_result( self ):
        if self.completed:
            return self.result
        return None
