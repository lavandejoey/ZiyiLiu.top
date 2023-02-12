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
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# local source

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config="../instance"):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    # app.config.from_pyfile('../instance/config.py')

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login.session_protection = 'basic'
    login.login_view = 'auth.login'
    login.init_app(app=app)

    from app import Models, Views, APIs
    with app.app_context():
        try:
            db.create_all()
            print("Init data complete!")
        except Exception as e:
            print(f"The Exception occurs:{e}")

    from app.Models import Users

    @login.user_loader
    def load_user(usr_id):
        # since the user_id is just the primary key of our user table,
        # use it in the query for the user
        return Users.query.get(int(usr_id))

    from app.Views.main import main_bp
    app.register_blueprint(main_bp)

    from app.Views.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.Views.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.Views.blog import blog_bp
    app.register_blueprint(blog_bp)

    @app.errorhandler(500)
    def not_found(error):
        return redirect(url_for('home.index'))

    return app
