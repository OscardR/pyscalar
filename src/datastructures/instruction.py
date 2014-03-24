#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from asm import NOP
from arch import reg

class Trap( Exception ):
    def __init__( self, msg ):
        Exception.__init__( self, msg )

class Instruction:
    def __init__( self, codop=NOP, ra=None, rb=None, rc=None ):
        self.codop = codop
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def __repr__( self ):
        op = self.codop
        ra = self.ra
        rb = self.rb
        rc = self.rc
        return "Instruction({}, {}, {}, {})".format( op, rc, ra, rb )

    def __str__( self ):
        op = self.codop
        ra = reg.name( self.ra ) if self.ra != None else u'\u2014'
        rb = reg.name( self.rb ) if self.rb != None else u'\u2014'
        rc = reg.name( self.rc ) if self.rc != None else u'\u2014'
        return u"{} {} {} {}".format( op, rc, ra, rb ).encode( 'utf-8' )
