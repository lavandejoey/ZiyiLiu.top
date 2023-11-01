#!/usr/bin/env python
# extentions.py
__author__ = "lavandejoeyZiyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library

# 3rd party packages
from flask_babel import Babel
from flask_caching import Cache
from flask_login import LoginManager
from flask_mail import Mail
from flask_sitemap import Sitemap
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager

# local source

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
