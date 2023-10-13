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
from flask import Flask
from flask_babel import Babel
from flask_mail import Mail
from flask_sitemap import Sitemap
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required

# local source
from .apis import *
from .views import *
from .models import *

# def create_main_app():
main_app = Flask(__name__, instance_relative_config=True, )
main_app.config.from_pyfile("config.py")

# initialize extensions
email = Mail(app=main_app, )
sitemap = Sitemap(app=main_app)
csrf = CSRFProtect(app=main_app, )
babel = Babel(app=main_app, locale_selector=get_locale, timezone_selector=get_timezone)
db.init_app(app=main_app)
with main_app.app_context():
    db.create_all()

# Initialize the login manager
login_manager = LoginManager(app=main_app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    # Replace this with a function to load the user based on the user_id
    return User.query.get(int(user_id))  # Assuming you have a User model


# register blueprints
main_app.register_blueprint(blueprint=error_blueprint)
main_app.register_blueprint(blueprint=ip_blueprint)
main_app.register_blueprint(blueprint=main_blueprint)
main_app.register_blueprint(blueprint=auth_blueprint)


# @app.route("/test")
# def test_page():
#     return render_template("TEST.html", current_language=get_locale(), current_locale=get_timezone())

# sitemap generator
@sitemap.register_generator
def sitemap_generator():
    yield 'main.index_page', {}
    yield 'main.portfolio_page', {}
    yield 'main.cv_page', {}
    yield 'main.contact_page', {}
    # yield 'file.file_page', {}
    # yield 'game.game_page', {}
