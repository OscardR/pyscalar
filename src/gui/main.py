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
         '/step', 'Step',
         '/run', 'Run' )

# Init app and web app
app = PyScalar()
webapp = web.application( urls, globals() )

class Start:
    def GET( self ):
        app.start()
        template_data = {
            'title' : DEF.APP_NAME,
            'app' : app,
            'def' : DEF }
        return render.main( template_data )

class Step:
    def GET( self ):
        app.step( web.input().steps )
        template_data = {
            'title' : DEF.APP_NAME,
            'app' : app,
            'def' : DEF }
        return render.main( template_data )

class Run:
    def GET( self ):
        app.run()
        template_data = {
            'title' : DEF.APP_NAME,
            'app' : app,
            'def' : DEF }
        return render.main( template_data )

application = webapp.wsgifunc()

if __name__ == '__main__':
    if DEF.WEB_ENABLED:
        webapp.run()
    else:
        app.run()
