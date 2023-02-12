#!/usr/bin/env python
# config.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
import os


# 3rd party packages
# local source


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    # configure the database connection
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI') or 'mysql://lavandejoey:SHlzyatshcn2069@101.43.21.228/lzyatshcn'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql://web_admin:SHlzyatshcn2069@localhost/lzyatshcn'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_VIEW = 'main.login'
