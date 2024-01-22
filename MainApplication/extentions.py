#!/usr/bin/env python
# extentions.py
__author__ = "lavandejoeyZiyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

from flask import jsonify
# 3rd party packages
from flask_babel import Babel
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_login import LoginManager
from flask_mail import Mail
from flask_sitemap import Sitemap
from flask_wtf.csrf import CSRFProtect

# local source
from MainApplication.apis.ip import get_client_ip

# standard library

# initialize extensions
email = Mail()
sitemap = Sitemap()
csrf = CSRFProtect()
babel = Babel()
cache = Cache()
# Initialize the login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login_page"
jwt = JWTManager()
limiter = Limiter(key_func=get_client_ip,
                  default_limits=["1000 per day", "200 per hour", "60 per minute", "3 per second"])


# Define the unauthorized_loader function to customize the JSON content
@jwt.unauthorized_loader
def unauthorized_callback(error_string):
    """
    Customize the JSON content of unauthorized access
    :param error_string: error message string
    :return: JSON content, 401
    """
    return jsonify({"status": "failed", "message": "Unauthorized access", "error": error_string}), 401
