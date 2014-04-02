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
        self.dest = None
        self.available = True
        self.completed = False
        self.result = None
        self.cycles = cycles
        self.countdown = cycles

    def feed( self, op1, op2, dest ):
        if self.available:
            self.op1 = op1
            self.op2 = op2
            self.dest = dest
            self.countdown = self.cycles
            self.available = False
            self.completed = False

    def step( self ):
        if self.op1 != None and \
            self.op2 != None and not self.completed:
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

    def is_empty( self ):
        return self.available and not self.completed

    def is_available( self ):
        return self.available

    def is_completed( self ):
        return self.completed

    def get_result( self ):
        if self.completed:
            self.available = True
            return self.result
        return None

    def __str__( self ):
        out = "FunctionalUnit<{}>".format( asm.name( self.op ) )
        return out

if __name__ == '__main__':
    fuADD = FunctionalUnit( asm.ADD )
    fuMUL = FunctionalUnit( asm.MUL, cycles=3 )
    a = 0
    b = 0
    fuADD.feed( 10, 20, a )
    fuMUL.feed( 12, 12, b )
    all_finished = False
    while not all_finished:
        for fu in [fuADD, fuMUL]:
            if not fu.is_completed():
                fu.step()
            print "{}, step: {}".format( fu, fu.countdown )
            print "{}, result: {}".format( fu, fu.get_result() )
        all_finished = fuADD.is_completed() and fuMUL.is_completed()
