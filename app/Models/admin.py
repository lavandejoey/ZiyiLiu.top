#!/usr/bin/env python
# admin.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
import random
import string

# 3rd party packages
from flask_login import UserMixin
from sqlalchemy import *
from sqlalchemy.sql import expression

# local source
from app import db
from app.APIs import str_verify, str_hash


# The table saves the basic info of users.
class Users(db.Model, UserMixin):
    __tablename__ = "Users"
    usr_id = Column("usr_id", Integer, primary_key=True, autoincrement=True, unique=True)
    usr_grp_id = Column("usr_grp_id", Integer, nullable=False, default="6666")
    usr_name = Column("usr_name", VARCHAR(50), nullable=False, unique=True)
    usr_email = Column("usr_email", VARCHAR(50), nullable=False, unique=True)
    usr_pw_hash = Column("usr_pw_hash", VARCHAR(256), nullable=False)
    usr_regi_date = Column("usr_regi_date", TIMESTAMP, default=expression.func.now())
    usr_last_login = Column("usr_last_login", TIMESTAMP, default=expression.func.now())
    usr_last_ip_addr = Column("usr_last_ip_addr", VARCHAR(15))
    usr_last_cookie_hash = Column("usr_last_cookie_hash", VARCHAR(256))
    usr_given_name = Column("usr_given_name", VARCHAR(50))
    usr_family_name = Column("usr_family_name", VARCHAR(50))
    usr_date_birth = Column("usr_date_birth", Date)
    usr_intro = Column("usr_intro", TEXT(500))

    def __init__(self, usr_grp_id=6666,
                 usr_name=''.join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
                 usr_email="@example.com", usr_pw_hash=str_hash("123456"),
                 usr_regi_date=None, usr_last_login=None, usr_last_ip_addr=None, usr_last_cookie_hash=None,
                 usr_given_name=None, usr_family_name=None, usr_date_birth=None, usr_intro=None):
        self.usr_grp_id = usr_grp_id
        self.usr_name = usr_name
        self.usr_email = usr_email
        self.usr_pw_hash = usr_pw_hash
        self.usr_regi_date = usr_regi_date
        self.usr_last_login = usr_last_login
        self.usr_last_ip_addr = usr_last_ip_addr
        self.usr_last_cookie_hash = usr_last_cookie_hash
        self.usr_given_name = usr_given_name
        self.usr_family_name = usr_family_name
        self.usr_date_birth = usr_date_birth
        self.usr_intro = usr_intro
        # for flask-login
        self.id = self.usr_id
        self.name = self.usr_name

    def __repr__(self):
        return '<Users %r %r>' % (self.usr_id, self.usr_name)

    @staticmethod
    def query_by_username(username):
        return Users.query.filter(Users.username == username).first()

    @property
    def pwd(self):
        raise AttributeError(u"The password is unreadable")

    @pwd.setter
    def pwd(self, pwd):
        self.usr_pw_hash = str_hash(pwd)

    def verify_password(self, pwd):
        return str_verify(self.usr_pw_hash, pwd)

    def get_id(self):
        return self.usr_id


"""
# The table saves one of the authentications.
class Usergroups(db.Model):
    __tablename__ = "U  serGroups"
    grp_id = Column("grp_id", Integer, primary_key=True)
    grp_name = Column("grp_name", VARCHAR(50))

    def __init__(self, grp_id, grp_name):
        self.grp_id = grp_id
        self.grp_name = grp_name

    def __repr__(self):
        return '<UserGroups %r %r>' % (self.grp_id, self.grp_name)


class UsersUsergroups(db.Model):
    __tablename__ = "Users_UserGroups"
    users_usr_id = Column("Users_usr_id", Integer, ForeignKey("Users.usr_id"), primary_key=True)
    usergroups_grp_id = Column("UserGroups_grp_id", Integer, ForeignKey("UserGroups.grp_id"), primary_key=True)

    users = relationship("Users", foreign_keys=users_usr_id)
    usergroups = relationship("Usergroups", foreign_keys=usergroups_grp_id)

# The table saves the info of APIs
class Apis(db.Model):
    __tablename__ = "APIs"
    api_id = Column("api_id", Integer, primary_key=True)
    api_endpoint = Column("api_endpoint", VARCHAR)
    # Unknown SQL type: "longtext"
    api_descrip = Column("api_descrip", String)
    api_method = Column("api_method", Enum("GET", "POST", "PUT", "DELETE"))
    api_created_at = Column("api_created_at", DateTime)
    api_updated_at = Column("api_updated_at", DateTime)

"""
