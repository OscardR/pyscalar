#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

import asm
from arch import reg

class Trap( Exception ):
    def __init__( self, msg="Trap instruction" ):
        Exception.__init__( self, msg )

class Instruction:
    def __init__( self, codop=asm.NOP, dest=None, op1=None, op2=None ):
        self.codop = codop
        self.dest = dest
        self.op1 = op1
        self.op2 = op2

    def __repr__( self ):
        return "Instruction({}, {}, {}, {})"\
            .format( 
                    asm.name( self.codop ),
                    reg.name( self.dest ),
                    reg.name( self.op1 ),
                    reg.name( self.op2 ) )

    def __str__( self ):
        op1 = reg.name( self.op1 ) if self.op1 != None else u'\u2014'
        op2 = reg.name( self.op2 ) if self.op2 != None else u'\u2014'
        dest = reg.name( self.dest ) if self.dest != None else u'\u2014'
        return u"{:<4}\t{:<4}\t{:<4}\t{:>4}"\
            .format( self.codop, dest, op1, op2 ).encode( 'utf-8' )

if __name__ == '__main__':
    i = Instruction( asm.ADDI, reg.r0, reg.r1, 1000 )
    print i
    print repr( i )
