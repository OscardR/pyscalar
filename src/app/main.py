#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

import web
from web.contrib.template import render_jinja

from arch.cpu import CPU
from programmer import Programmer
from log import Log

# Init our application, this is just about the most basic setup
render = render_jinja( '.', encoding='utf-8' )
urls = ( '/', 'Index' )
app = web.application( urls, globals() )
l = Log( 'PyScalar' )

def raw_app():
    l.v( "Iniciando ejecución", "main" )
    cpu = CPU()
    prog = Programmer( cpu.imem )
    prog.program( 'code.asm' )
    cpu.run()
    l.v( "Fin de la ejecución", "main" )

class Index:
    def GET( self ):
        raw_app()
        return render.main( title='PyScalar' )

application = app.wsgifunc()

if __name__ == '__main__':
    raw_app()
    # app.run()
