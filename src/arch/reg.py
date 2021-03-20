#!/usr/bin/env python
# coding:utf8

"""
Created on 09/03/2014
@author: Óscar Gómez Alcañiz <oscar.gomez@uji.es>
"""

import app.log as log

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


def name(reg):
    l = None
    for l in globals():
        if globals()[l] == reg and l != "reg":
            return l
    return "{}".format(reg)


class RegisterNotFoundException(Exception):
    def __init__(self, reg):
        super(RegisterNotFoundException, self).__init__(
            "Register not found: [{}]".format(reg)
        )


class Registers(dict):
    def __init__(self, *args, **kw):
        super(Registers, self).__init__(*args, **kw)
        self.itemlist = [
            r0,
            r1,
            r2,
            r3,
            r4,
            r5,
            r6,
            r7,
            r8,
            r9,
            r10,
            r11,
            r12,
            r13,
            r14,
            r15,
            zero,
        ]
        for r in self.itemlist:
            self[r] = r

    def __getitem__(self, key):
        if key not in self.itemlist:
            raise RegisterNotFoundException(key)
        return super(Registers, self).__getitem__(key)

    def __setitem__(self, key, value):
        if not key in self.itemlist:
            raise Exception("New registers cannot be added")
        super(Registers, self).__setitem__(key, value)

    def __iter__(self):
        return iter(self.itemlist)

    def keys(self):
        return self.itemlist

    def values(self):
        return [self[key][0] for key in self]

    def itervalues(self):
        return (self[key][0] for key in self)

    def check_ok(self, reg):
        return self[reg] is not None

    def invalidate(self, reg):
        if reg not in self.itemlist:
            raise RegisterNotFoundException(reg)
        self[reg] = None

    def __str__(self):
        out = log.make_title("Registers")
        for reg in self.itemlist:
            if self[reg] is not None:
                fmt_str = "[ {:>4} ]: {:#06x} "
            else:
                fmt_str = "[ {:>4} ]: {:>6} "
            out += fmt_str.format(name(reg), self[reg])
            if reg % 4 == 3:
                out += "\n"
        return out


if __name__ == "__main__":
    reg = Registers()
    reg[r10] = 10
    print(reg)
    print(reg.check_ok(r0))
    reg.invalidate(r0)
    print(reg)
    print(reg[r0])
    print(reg.check_ok(r0))
    print(name(r5))
    print(reg[1000])
