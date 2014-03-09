#!/usr/bin/env python
#coding:utf8

"""
Created on 09/03/2014
@author: Óscar Gómez Alcañiz <oscar.gomez@uji.es>
"""

# Registers name definitions
r0 = 0x00
r1 = 0x01
r2 = 0x02
r3 = 0x03
r4 = 0x04
r5 = 0x05
r6 = 0x06
r7 = 0x07
r8 = 0x08
r9 = 0x09
r10 = 0x0A
r11 = 0x0B
r12 = 0x0C
r13 = 0x0D
r14 = 0x0E
r15 = 0x0F
zero = 0xFF

class Registers( dict ):
    def __init__( self, *args, **kw ):
        super( Registers, self ).__init__( *args, **kw )
        self.itemlist = [ r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, zero ]
        for r in self.itemlist: self[r] = 0x00

    def __setitem__( self, key, value ):
        if key in self.itemlist:
            super( Registers, self ).__setitem__( key, value )
        else:
            raise Exception( "New registers cannot be added" )
    def __iter__( self ):
        return iter( self.itemlist )

    def keys( self ):
        return self.itemlist

    def values( self ):
        return [self[key] for key in self]

    def itervalues( self ):
        return ( self[key] for key in self )
