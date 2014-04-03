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
from pyscalar import PyScalar

# Init our web application, this is just about the most basic setup
render = render_jinja( '.', encoding='utf-8' )
urls = ( '/', 'Index' )
webapp = web.application( urls, globals() )

class Index:
    def GET( self ):
        app.run()
        return render.main( title='PyScalar' )

application = webapp.wsgifunc()

if __name__ == '__main__':
    app = PyScalar()
    app.run()
    # webapp.run()
