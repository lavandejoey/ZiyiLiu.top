#!/usr/bin/env python
# __init__.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library

# 3rd party packages
from flask import Flask

# local source
from MainApplication.apis import *
from MainApplication.extentions import *
from MainApplication.models import *
from MainApplication.views import *

# def create_main_app():
main_app = Flask(__name__, instance_relative_config=True, )
main_app.config.from_pyfile("config.py")

# initialize extensions
email.init_app(app=main_app, )
sitemap.init_app(app=main_app)
csrf.init_app(app=main_app, )
babel.init_app(app=main_app, locale_selector=get_client_locale, timezone_selector=get_client_timezone)
db.init_app(app=main_app)
with main_app.app_context():
    db.create_all()
# Initialize the login manager
login_manager.init_app(app=main_app)
login_manager.login_view = "auth.login_page"
cache.init_app(app=main_app,
               config={"CACHE_TYPE": main_app.config["CACHE_TYPE"],
                       "CACHE_DIR": main_app.config["CACHE_DIR"],
                       "CACHE_DEFAULT_TIMEOUT": main_app.config["CACHE_DEFAULT_TIMEOUT"],
                       "CACHE_THRESHOLD": main_app.config["CACHE_THRESHOLD"],
                       "CACHE_NO_NULL_WARNING": main_app.config["CACHE_NO_NULL_WARNING"]})
jwt.init_app(app=main_app)
limiter.init_app(app=main_app)


@login_manager.user_loader
def load_user(user_id):
    # Replace this with a function to load the user based on the user_id
    return User.query.get(int(user_id))  # Assuming you have a User model


# register blueprints
main_app.register_blueprint(blueprint=error_blueprint)
main_app.register_blueprint(blueprint=ip_blueprint)
main_app.register_blueprint(blueprint=main_blueprint)
main_app.register_blueprint(blueprint=auth_blueprint)
main_app.register_blueprint(blueprint=apis_blueprint)
csrf.exempt(apis_blueprint)


@main_app.route("/test")
def test_page():
    if not main_app.debug:
        # if not debug mode, return 404
        return jsonify({"status": "failed", "message": "Not Found"}), 404
    return render_template("TEST.html", title=gettext("TEST"), page="test")
