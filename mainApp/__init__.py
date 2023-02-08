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
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# local source

db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev'
    app.config['DATABASE'] = os.path.join(app.instance_path, )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # configure the database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@host/database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize the database connection
    db.init_app(app)

    from mainApp import routes
    routes.create_routes(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('index'))

    return app
