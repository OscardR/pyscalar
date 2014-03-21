#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

class ROBLine:
    def __init__( self, dest, value, ok, last ):
        self.dest = dest
        self.value = value
        self.ok = ok
        self.last = last

    def set_value( self, value ):
        self.value = value

class ReorderBuffer:
    def __init__( self, size=8 ):
        self.size = size
        self.lines = [None] * self.size
        self.pos = 0
        self.full = False

    def __getitem__( self, index ):
        return self.lines[index]

    def get_last_index( self, reg ):
        for i, line in enumerate( self.lines ):
            if line.dest == reg and line.last:
                return i

    def insert_line( self, dest, value=None, ok=False, last=True ):
        if not self.full:
            self.lines[self.pos] = ROBLine( dest, value, ok, last )
            while self.lines[self.pos] != None:
                self.pos += 1
                self.pos %= self.size  # Bucle infinito. OJO!
