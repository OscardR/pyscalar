"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""
from cpu import CPU
from log import Log

if __name__ == '__main__':
    l = Log('PyScalar')
    l.v("Iniciando ejecución", 'GREEN_BOLD', "main")
    cpu = CPU()
    cpu.program('code.asm')
    cpu.run()
    l.v('Fin de la ejecución', 'main')