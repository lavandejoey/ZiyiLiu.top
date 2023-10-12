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

from .apis import *
# local source
from .views import *


def create_main_app():
    app = Flask(__name__, instance_relative_config=True, )
    app.config.from_pyfile("config.py")

    # initialize extensions
    email = Mail(app=app, )
    sitemap = Sitemap(app=app)
    csrf = CSRFProtect(app=app, )
    babel = Babel(app=app, locale_selector=get_locale, timezone_selector=get_timezone)

    # register blueprints
    app.register_blueprint(blueprint=error_blueprint)
    app.register_blueprint(blueprint=ip_blueprint)
    app.register_blueprint(blueprint=main_blueprint)
    app.register_blueprint(blueprint=file_blueprint)
    app.register_blueprint(blueprint=game_blueprint)

    if app.config["DEBUG"]:
        @app.route("/test")
        def test_page():
            return render_template("TEST.html", current_language=get_locale(), current_locale=get_timezone())

    # sitemap generator
    @sitemap.register_generator
    def sitemap_generator():
        yield 'main.index_page', {}
        yield 'main.portfolio_page', {}
        yield 'main.cv_page', {}
        yield 'main.contact_page', {}
        # yield 'file.file_page', {}
        # yield 'game.game_page', {}

    return app
