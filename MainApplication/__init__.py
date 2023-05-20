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
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# local source
from .views import main_blueprint

email = Mail()
# Initialize CSRF protection
csrf = CSRFProtect()


def create_main_app(config="config.py"):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object('config.Config')
    app.config.from_pyfile(config)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    app.config["MAIL_SERVER"] = "smtp-mail.outlook.com"
    # This is the port number that your mail server uses to receive email.
    app.config["MAIL_PORT"] = 587 # TLS:587 SSl:465 None:25
    # This is a Boolean flag that tells Flask-Mail whether to use TLS encryption when sending emails.
    app.config["MAIL_USE_TLS"] = True
    # This is a Boolean flag that tells Flask-Mail whether to use SSL encryption when sending emails.
    app.config["MAIL_USE_SSL"] = False
    # This is the username that your application will use to log in to the mail server.
    app.config["MAIL_USERNAME"] = "lavandejoey@outlook.com"
    # This is the password that your application will use to log in to the mail server.
    app.config["MAIL_PASSWORD"] = "LNms120921"
    # This is the email address that the application will use as the "from" address for system emails. ADMIN_EMAIL = ""
    app.config["MAIL_DEFAULT_SENDER"] = ("lavandejoey", "JoshuaZiyiLiu.com@outlook.com")

    # initialize extensions
    email.init_app(app=app)
    csrf.init_app(app=app)

    # register blueprints
    app.register_blueprint(blueprint=main_blueprint)

    @app.errorhandler(500)
    def not_found(error):
        return redirect(url_for('main.index_page'))

    return app
