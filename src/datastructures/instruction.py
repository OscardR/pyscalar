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
    def __init__( self, codop=asm.NOP, ra=None, rb=None, rc=None ):
        self.codop = codop
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def __repr__( self ):
        op = asm.name( self.codop )
        ra = reg.name( self.ra )
        rb = reg.name( self.rb )
        rc = reg.name( self.rc )
        return "Instruction({}, {}, {}, {})".format( op, ra, rb, rc )

    def __str__( self ):
        op = self.codop
        ra = reg.name( self.ra ) if self.ra != None else u'\u2014'
        rb = reg.name( self.rb ) if self.rb != None else u'\u2014'
        rc = reg.name( self.rc ) if self.rc != None else u'\u2014'
        return u"{} {} {} {}".format( op, rc, ra, rb ).encode( 'utf-8' )

if __name__ == '__main__':
    i = Instruction( asm.ADDI, reg.r1, 1000, reg.r0 )
    print i
    print repr( i )
