#!/usr/bin/env python
# __init__.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
import os

# 3rd party packages
import toml
from flask import Flask, redirect, url_for
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_sitemap import Sitemap

# local source
from .views import main_blueprint

email = Mail()
sitemap = Sitemap()
csrf = CSRFProtect()

def create_main_app():
    app = Flask(__name__, instance_relative_config=True,)
    app.config.from_pyfile("config.py")

    # initialize extensions
    email.init_app(app=app)
    sitemap.init_app(app=app)
    csrf.init_app(app=app)

    # register blueprints
    app.register_blueprint(blueprint=main_blueprint)

    @app.errorhandler(500)
    def not_found(error):
        return redirect(url_for('main.index_page'))

    return app
