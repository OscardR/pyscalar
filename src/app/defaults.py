#!/usr/bin/env python
# coding:utf8

"""
Defaults file
=============
Settings for all modules

Created on 04/04/2014
@author: "Óscar Gómez Alcañiz <oscar.gomez@uji.es>"
"""


class DEF:
    # App data
    APP_NAME = "PyScalar"

    # CPU architecture
    MEM_SIZE = 32
    IW_SIZE = 10
    ROB_SIZE = 10
    S = 2

    # Execution step by step
    STEP_BY_STEP = False

    # File with the code
    ASM_CODE = "code.asm"

    # Web UI or CLI?
    WEB_ENABLED = True


if __name__ == "__main__":
    print("Nothing to see here!")
