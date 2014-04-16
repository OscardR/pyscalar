#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

# Web framework imports
import web
from web.contrib.template import render_jinja

# Import PyScalar app
from app.pyscalar import PyScalar
import app.defaults as DEF

# Init our web application, this is just about the most basic setup
render = render_jinja( '../gui', encoding='utf-8' )
urls = ( '/', 'Start',
         '/code', 'Code',
         '/step', 'Step',
         '/run', 'Run',
         '/reset', 'Start' )

# Init app and web app
app = PyScalar()
webapp = web.application( urls, globals() )

class Default:
    def GET( self ):
        template_data = {
            'title' : DEF.APP_NAME,
            'app' : app,
            'def' : DEF }
        return render.main( template_data )

class Code( Default ):
    def POST( self ):
        f = web.input().codefile
        web.debug( f )
        codefile = open( "tmp.asm", "w" )
        codefile.write( f )
        app = PyScalar( "../gui/tmp.asm" )
        app.start()
        return Default.GET( self )

class Start( Default ):
    def GET( self ):
        app.start()
        return Default.GET( self )

class Step( Default ):
    def GET( self ):
        app.step( web.input().steps )
        return Default.GET( self )

class Run( Default ):
    def GET( self ):
        app.run()
        return Default.GET( self )

application = webapp.wsgifunc()

if __name__ == '__main__':
    if DEF.WEB_ENABLED:
        webapp.run()
    else:
        app.run()
