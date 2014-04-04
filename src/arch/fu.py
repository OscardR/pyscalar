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

    def __init__( self, codop=asm.ADD, cycles=1 ):
        self.codop = codop
        self.op1 = None
        self.op2 = None
        self.dest = None
        self.n_inst = None
        self.available = True
        self.completed = False
        self.result = None
        self.cycles = cycles
        self.countdown = cycles

    def feed( self, op1, op2, dest, n_inst ):
        if self.available:
            self.op1 = int( op1 )
            self.op2 = int( op2 )
            self.dest = dest
            self.n_inst = n_inst
            self.countdown = self.cycles
            self.available = False
            self.completed = False

    def step( self ):
        if self.op1 != None and \
            self.op2 != None and not self.completed:
            self.countdown -= 1
            if self.countdown == 0:
                if self.codop == asm.MULT:
                    self.result = self.op1 * self.op2
                elif self.codop == asm.ADD:
                    self.result = self.op1 + self.op2
                elif self.codop == asm.SUB:
                    self.result = self.op1 - self.op2
                elif self.codop == asm.DIV:
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
            self.completed = False
            return self.result
        return None

    def __str__( self ):
        operands = {
            asm.MULT : "×",
            asm.ADD : "+",
            asm.SUB : "—",
            asm.DIV : "÷"
        }
        if self.is_empty():
            out = "FU({}) [ ---empty--- ]".format( operands[self.codop] )
        else:
            out = "FU({}) [I{}] [ {}{}{}={} | countdown({}): {} ]"\
                .format( operands[self.codop],
                    self.n_inst,
                    self.op1,
                    operands[self.codop],
                    self.op2,
                    self.result if self.result != None else "??",
                    self.cycles,
                    self.countdown )
        return out

if __name__ == '__main__':
    fuADD = FunctionalUnit( asm.ADD )
    fuMUL = FunctionalUnit( asm.MULT, cycles=3 )
    a = 0
    b = 0
    fuADD.feed( 10, 20, a, 1 )
    fuMUL.feed( 12, 12, b, 2 )
    all_finished = False
    while not all_finished:
        for fu in [fuADD, fuMUL]:
            if not fu.is_completed():
                fu.step()
            print fu
            result = fu.get_result()
        all_finished = fuADD.is_empty() and fuMUL.is_empty()
