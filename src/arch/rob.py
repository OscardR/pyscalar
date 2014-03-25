#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from arch import reg
from app import log

ISSUED = 'i'
EXECUTING = 'x'
FINISHED = 'f'

class ROBLine:
    def __init__( self, dest, value, ok, last ):
        self.dest = dest
        self.value = value
        self.ok = ok
        self.last = last
        self.status = ISSUED

    def set_value( self, value ):
        self.value = value

    def __str__( self ):
        return "{:>5} | {:>5} | {:>5} | {:>5} | {:1}".format( self.dest, self.value, self.ok, self.last, self.status )

class ReorderBuffer:
    def __init__( self, size=8 ):
        self.size = size
        self.lines = [None] * self.size
        self.pos = 0
        self.full = False

    def __getitem__( self, index ):
        return self.lines[index]

    def insert_line( self, dest, value=None, ok=False ):
        if not self.full:
            for line in self.lines:
                if line != None and line.dest == dest:
                    line.last = False
            self.lines[self.pos] = ROBLine( dest, value, ok, last=True )
            if None in self.lines:
                while self.lines[self.pos] != None:
                    self.pos += 1
                    self.pos %= self.size
            else:
                self.full = True

    def get_last_index( self, reg ):
        for i, line in enumerate( self.lines ):
            if line.dest == reg and line.last:
                return i
        return None

    def get_register( self, reg ):
        for line in self.lines:
            if line.dest == reg and line.last:
                if line.ok:
                    return line.value
                else:
                    return False
        return None

    def get_finished( self ):
        finished = []
        for line in self.lines:
            if line.status == FINISHED:
                finished.append( line )
        return finished

    def __str__( self ):
        out = log.make_title( "ReorderBuffer [{}]".format( self.size ) )
        for i, line in enumerate( self.lines ):
            out += "[ {:>02} ] {}\n".format( i, line )
        return out


if __name__ == '__main__':
    rob = ReorderBuffer( 8 )
    rob.insert_line( reg.r1 )
    rob.insert_line( reg.r2 )
    rob.insert_line( reg.r1, 123, ok=True )
    print rob
    print rob.get_last_index( reg.r1 )
    print rob.get_register( reg.r1 )
