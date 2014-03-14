#!/usr/bin/env python
#coding:utf8

"""
Created on 14/03/2014
@author: "Óscar Gómez Alcañiz <oscar.gomez@uji.es>"
"""

MULT = 0x01
SUM = 0x02

class FunctionalUnit():
    def __init__(self, type=SUM):
        self.type = type
        
    def step(self):
        pass
    