#!/usr/bin/env python
# admin.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
# local source
from app import db


# create the User model
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usrname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    passwd = db.Column(db.String(255), nullable=False)
    group_id = db.Column(db.Integer, nullable=True, )
