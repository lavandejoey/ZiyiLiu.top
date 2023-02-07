#!/usr/bin/env python

# standard library
import os
# 3rd party packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wekzeug.contrib.fixers import ProxyFix
# local source
from .database import init_db
from .middleware import after_request_middleware, before_request_middleware, teardown_appcontext_middleware
from .middleware import response
from .foss import bp as foss_bp


def create_app(config_filename):
    # initialize flask application
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    # rigister database
    db=SQLAlchemy()

    # register all blueprints
    app.register_blueprint(foss_bp)

    # register custom response class
    app.response_class = response.JSONResponse

    # register before request middleware
    before_request_middleware(app=app)

    # register after request middleware
    after_request_middleware(app=app)

    # register after app context teardown middleware
    teardown_appcontext_middleware(app=app)

    # register custom error handler
    response.json_error_handler(app=app)

    # initialize the database
    init_db()

    return app