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