#!/usr/bin/env python
# coding:utf8

"""
Created on 07/03/2014
@author: Óscar Gómez <oscar.gomez@uji.es>
"""

# Web framework imports
import web
import pathlib
from web.contrib.template import render_jinja

# Import PyScalar app
from app.pyscalar import PyScalar
from app.defaults import DEF

cwd = pathlib.Path(__file__).parent.absolute()

# Init our web application, this is just about the most basic setup
render = render_jinja(cwd, encoding="utf-8")
# fmt: off
urls = (
    "/",      "Start",
    "/code",  "Code",
    "/step",  "Step",
    "/run",   "Run",
    "/reset", "Start",
)
# fmt: on

# Init app and web app
app = PyScalar()
webapp = web.application(urls, globals())
application = webapp.wsgifunc()


class Default:
    def GET(self):
        template_data = {"title": DEF.APP_NAME, "app": app, "def": DEF}
        return render.main(template_data)


class Code:
    def POST(self):
        f = web.input().codefile
        web.debug(f)
        codefile = open(f"{cwd}/tmp.asm", "wb")
        codefile.write(f)
        app = PyScalar(f"{cwd}/tmp.asm")
        app.start()
        return Default().GET()


class Start:
    def GET(self):
        app.start()
        return Default().GET()


class Step:
    def GET(self):
        app.step(web.input().steps)
        return Default().GET()


class Run:
    def GET(self):
        app.run()
        return Default().GET()


if __name__ == "__main__":
    if DEF.WEB_ENABLED:
        webapp.run()
    else:
        app.run()
