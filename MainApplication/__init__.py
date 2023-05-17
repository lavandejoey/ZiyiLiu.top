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

# local source
from .views import main_blueprint

email = Mail()


def create_main_app(config="config.py"):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object('config.Config')
    app.config.from_pyfile(config)
    app.secret_key = 'your_secret_key_here'

    # initialize extensions
    email.init_app(app=app)

    # register blueprints
    app.register_blueprint(blueprint=main_blueprint)

    @app.errorhandler(500)
    def not_found(error):
        return redirect(url_for('main.index'))

    return app
