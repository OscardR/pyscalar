#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez Alcañiz <oscar.gomez@uji.es>
"""
import app.log as log
from datastructures.instruction import Instruction

class InstructionsMemory:
    def __init__( self ):
        self.instructions = []

    def insert_instruction( self, instruction ):
        self.instructions.append( instruction )

    def fetch_instruction( self, pc ):
        try:
            return self.instructions[pc]
        except IndexError:
            return Instruction()

    def __str__( self ):
        out = log.make_title( "InstructionMemory" )
        for i, inst in enumerate( self.instructions ):
            out += "[ {:#04x} ] {}\n".format( i, inst )
        return out

l = log.Log( "DataMemory" )
class DataMemory:
    def __init__( self, size=32 ):
        self.memory = [word for word in xrange( size )]

    def read_byte( self, index ):
        l.d( "Read: {}".format( index ), "Memory" )
        return self.memory[index]

    def write_byte( self, index, data ):
        l.d( "Write: {} <= {}".format( index, data ), "Memory" )
        self.memory[index] = data

    def __str__( self ):
        out = log.make_title( "DataMemory" )
        for i, w in enumerate( self.memory ):
            out += "[ {:#04x} ]: {:#06x} ".format( i, w )
            if i % 4 == 3: out += "\n"
        return out
