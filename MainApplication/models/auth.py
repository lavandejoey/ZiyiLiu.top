#!/usr/bin/env python
# models/auth.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

from flask import current_app
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .base import *

ph = PasswordHasher()


class User(Base, UserMixin):
    __tablename__ = 'accounts'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, username, email, phone=None):
        self.username = username
        self.email = email
        self.phone = phone

    # Define methods to set and check passwords securely
    def set_password(self, password):
        self.password = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self.password, password)
        except VerifyMismatchError:
            return False

    def get_id(self):
        return str(self.uid)

    def belong_to_group(self, g_id="", g_name=""):
        # Check if the user belongs to the specified group
        # Query the AccountGroupRelationship table for the user's account_id and the group's group_id
        if not g_id and not g_name:
            raise ValueError("Either g_id or g_name must be provided")
        group_relationship = db.session.query(AccountGroupRelationship).filter(
            AccountGroupRelationship.account_id == self.uid, AccountGroupRelationship.group_id == g_id).first()

        if group_relationship:  # The user belongs to the group
            return True
        else:  # If g_name is provided, check if the user belongs to the group by name
            if g_name:
                group = db.session.query(Group).filter(Group.group_name == g_name).first()
                if group:
                    group_relationship = db.session.query(AccountGroupRelationship).filter(
                        AccountGroupRelationship.account_id == self.uid,
                        AccountGroupRelationship.group_id == group.group_id).first()
                    if group_relationship:
                        return True

        return False


class Group(Base):
    __tablename__ = 'groups'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(64), nullable=False)

    def __init__(self, group_name):
        self.group_name = group_name


class AccountGroupRelationship(Base):
    __tablename__ = 'account_group_relationship'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.uid'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)

    def __init__(self, account_id, group_id):
        self.account_id = account_id
        self.group_id = group_id
