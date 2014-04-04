#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

from arch import reg
from app import log
from random import random

# Flags to track the state of the instruction
DECODED = 'd'
ISSUED = 'i'
EXECUTING = 'x'
FINISHED = 'f'

class ROBLine:
    def __init__( self, index, n_inst, dest, value=None, ok=False, last=True, flag=DECODED ):
        self.index = index
        self.n_inst = n_inst
        self.dest = dest
        self.value = value
        self.ok = ok
        self.last = last
        self.flag = flag

    def set_value( self, new_value ):
        self.value = new_value

    def set_ok( self, ok=True ):
        self.ok = ok

    def set_last( self, last=True ):
        self.last = last

    def set_flag( self, new_flag ):
        self.flag = new_flag

    def __str__( self ):
        return "{:>5} | {:>5} | {:>5} | {:>5} | {:>5} | {:5}"\
            .format( "I" + str( self.n_inst ), \
                     self.dest, \
                     self.value, \
                     self.ok, \
                     self.last, \
                     self.flag )

class ReorderBuffer:
    def __init__( self, size=8 ):
        self.size = size
        self.lines = [None] * self.size
        self.full = False
        self.head = 0
        self.tail = 0

    def __getitem__( self, pos ):
        return self.lines[pos]

    def insert_line( self, n_inst, dest, value=None, ok=False ):
        # If ROB is not full
        if not self.full:
            # Check for other lines renaming the same register,
            # set their 'last' field to False
            for line in self.lines:
                if line != None and line.dest == dest:
                    line.last = False

            # Save current position
            pos = self.head

            # Insert new line
            self.lines[self.head] = ROBLine( pos, n_inst, dest, value, ok )

            # Check for free slots
            if None in self.lines:
                while self.lines[self.head] != None:
                    self.head += 1
                    self.head %= self.size
            else:
                # No slots means ROB full
                self.full = True

            # Return current insert position
            return pos

        # Return false if insertion not possible
        return False

    def get_instruction( self, n_inst ):
        for line in self.lines:
            if line != None and line.n_inst == n_inst:
                return line
        return None

    def get_last_index( self, reg ):
        for line in self.lines:
            if line.dest == reg and line.last:
                return line.index
        return None

    def get_register( self, reg ):
        for line in self.lines:
            if line.dest == reg and line.last:
                if line.ok:
                    return line.value
                else:
                    return False
        return None

    def flush_finished( self, how_many=0 ):
        # Flush all finished instructions by default
        if how_many == 0: how_many = self.size

        # Initialize vars
        finished = []
        count = 0

        # Get all finished lines from the tail
        while self.lines[self.tail] != None \
            and self.lines[self.tail].flag == FINISHED:
            finished.append( self.lines[self.tail] )
            self.tail += 1
            self.tail %= self.size
            count += 1
            # Get only specified number of lines
            if count >= how_many: break

        # Erase flushed lines from ROB
        for line in finished:
            self.lines[line.index] = None
            if self.full:
                self.full = False

        return finished

    def clear_line( self, index ):
        # Erase line at index
        self.lines[index] = None

        # Correct head position
        self.head = index

        # Correct full state
        if self.full:
            self.full = False

    def is_empty( self ):
        for line in self.lines:
            if line != None: return False
        return True

    def __str__( self ):
        out = log.make_title( "ReorderBuffer [{}]".format( self.size ) )
        out += "       [ {:>5} ¦ {:>5} ¦ {:>5} ¦ {:>5} ¦ {:>5} ¦ {:5} ]\n"\
            .format( "NI", "DEST", "VAL", "OK", "LAST", "FLAG" )
        for i, line in enumerate( self.lines ):
            out += "[ {:>02} ] [ {:^45} ]{}{}\n"\
                .format( i, \
                         line if line != None else "--- empty ---", \
                         " <H>" if i == self.head else "", \
                         " <T>" if i == self.tail else "" )
        return out


if __name__ == '__main__':
    """
    Test Suite to check correct behaviour of the ReorderBuffer
    """
    rob = ReorderBuffer( 8 )
    rob.insert_line( 0, reg.r1 )
    rob.insert_line( 1, reg.r2 )
    rob.insert_line( 2, reg.r1, 123, ok=True )
    print rob
    print rob.get_last_index( reg.r1 )
    print rob.get_register( reg.r1 )

    rob[0].set_flag( FINISHED )
    rob[1].set_flag( FINISHED )
    rob[2].set_flag( ISSUED )
    finished = rob.flush_finished()
    print rob
    print log.make_title( "Finished Instructions:" )
    for f in finished: print f

    success = []
    for i in range( 8 ):
        success.append( rob.insert_line( i + 3, int( random() * 16 ) ) )
        print i + 3, '=', success[i]

    print rob

    for i in range( 3 ):
        rob.clear_line( success[i] )

    print rob
