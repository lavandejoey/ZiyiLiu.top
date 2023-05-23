#!/usr/bin/env python
# __init__.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library

# 3rd party packages
from flask import Flask, redirect, url_for
from flask_mail import Mail
from flask_sitemap import Sitemap
from flask_wtf.csrf import CSRFProtect

# local source
from .views import *

email = Mail()
sitemap = Sitemap()
csrf = CSRFProtect()


def create_main_app():
    app = Flask(__name__, instance_relative_config=True, )
    app.config.from_pyfile("config.py")

    # initialize extensions
    email.init_app(app=app)
    sitemap.init_app(app=app)
    csrf.init_app(app=app)

    # register blueprints
    app.register_blueprint(blueprint=error_blueprint)
    app.register_blueprint(blueprint=main_blueprint)
    app.register_blueprint(blueprint=file_blueprint)
    app.register_blueprint(blueprint=game_blueprint)

    @sitemap.register_generator
    def register_generator():
        yield 'main.index_page', {}
        yield 'main.portfolio_page', {}
        yield 'main.cv_page', {}
        yield 'main.contact_page', {}

    return app
