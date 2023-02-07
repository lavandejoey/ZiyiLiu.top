#!/usr/bin/env python
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"
# standard library
import os
# 3rd party packages
from flask import Flask
import flask_sqlalchemy
from wekzeug.contrib.fixers import ProxyFix
# local source
import mainApp

app=create_app()

def run():
    debug=os.environ.get("APP_DEBUG",True)
    host=os.environ.get("APP_HOST","0.0.0.0")
    port=os.environ.get("APP_PORT",8080)

    app.run(debug=debug,host=host,port=port)

wsgi=ProxyFix(app.wsgi_app)

if __name__=='__main__':
    print(app)#run()