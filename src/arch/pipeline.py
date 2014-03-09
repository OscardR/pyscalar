#!/usr/bin/env python
#coding:utf8

"""
Created on 08/03/2014
@author: Óscar Gómez Alcañiz <oscar.gomez@uji.es>
"""

from app.log import Log

l = Log("pipeline")

class Stage:
    def __init__(self, name, prev_reg, next_reg):
        self.name = name
        l.v("Stage %s initialized!" % name, "Stage")
        self.prev_reg = prev_reg
        self.next_reg = next_reg

    def prepare(self):
        raise NotImplementedError(
            "Stage {0} has not implemented 'prepare' method!".format(self.name))

    def execute(self):
        raise NotImplementedError(
            "Stage {0} has not implemented 'execute' method!".format(self.name))

    def finalize(self):
        raise NotImplementedError(
            "Stage {0} has not implemented 'finalize' method!".format(self.name))
        
class IF(Stage):
    def __init__(self, cpu, if_id):
        Stage.__init__(self, "IF", None, if_id)
        self.cpu = cpu
        self.N = self.cpu.N
    
    def prepare(self):
        self.imem = self.cpu.imem
        self.iw = self.cpu.iw
        for i in range(self.N):
            inst = self.imem.fetch_instruction(self.cpu.PC)
            self.iw.insert_instruction(inst)
            self.cpu.increment_PC()
    
    def execute(self):
        pass
    
    def finalize(self):
        pass
    
class ID(Stage):
    def __init__(self, if_id, id_iss):
        Stage.__init__(self, "ID", if_id, id_iss)
        
    def prepare(self):
        pass
    
    def execute(self):
        pass
    
    def finalize(self):
        pass