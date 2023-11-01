#!/usr/bin/env python
# models/auth.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_login import UserMixin

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

    def to_dict(self, with_groups: bool = False):
        if with_groups:
            l_groups = self.get_groups()
            return {'uid': self.get_id(), 'username': self.username, 'email': self.email, 'phone': self.phone,
                    'groups': l_groups, 'created_at': self.created_at, 'updated_at': self.updated_at}
        else:
            return {'uid': self.get_id(), 'username': self.username, 'email': self.email, 'phone': self.phone,
                    'created_at': self.created_at, 'updated_at': self.updated_at}

    # Define methods to set and check passwords securely
    def set_password(self, password):
        self.password = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self.password, password)
        except VerifyMismatchError:
            return False

    def get_id(self):
        # Return the user ID fill 0 to 8 digits
        return str(self.uid).zfill(8)

    def get_groups(self) -> dict:
        # Get all groups the user belongs to
        rst = {
            'msg': 'fail',
            'cnt': 0,
            'groups': []
        }
        group_relationships = db.session.query(UserGroupRelationship).filter(
            UserGroupRelationship.account_id == self.uid).all()
        for group_relationship in group_relationships:
            group = db.session.query(Group).filter(Group.group_id == group_relationship.group_id).first()
            rst['groups'].append({
                'id': group.group_id,
                'name': group.group_name
            })
        rst['groups'] = sorted(rst['groups'], key=lambda x: x['id'])
        rst['msg'] = 'success'
        rst['cnt'] = len(rst['groups'])
        return rst

    def belong_to_group(self, g_id: int = None, g_name: str = None):
        # Check if the user belongs to the specified group
        # Query the AccountGroupRelationship table for the user's account_id and the group's group_id
        if not g_id and not g_name:
            raise ValueError("Either g_id or g_name must be provided")
        group_relationship = db.session.query(UserGroupRelationship).filter(
            UserGroupRelationship.account_id == self.uid, UserGroupRelationship.group_id == g_id).first()

        if group_relationship:  # The user belongs to the group
            return True
        else:  # If g_name is provided, check if the user belongs to the group by name
            if g_name:
                group = db.session.query(Group).filter(Group.group_name == g_name).first()
                if group:
                    group_relationship = db.session.query(UserGroupRelationship).filter(
                        UserGroupRelationship.account_id == self.uid,
                        UserGroupRelationship.group_id == group.group_id).first()
                    if group_relationship:
                        return True

        return False


class Group(Base):
    __tablename__ = 'groups'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(64), nullable=False)

    def __init__(self, group_name):
        self.group_name = group_name


class UserGroupRelationship(Base):
    __tablename__ = 'account_group_relationship'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.uid'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)

    def __init__(self, account_id, group_id):
        self.account_id = account_id
        self.group_id = group_id


class Token(Base):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(255), nullable=False, unique=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.String(255), nullable=True)
    valid_days = db.Column(db.Integer, nullable=True)

    def __init__(self, value, user, expire_date=None, valid_days=None, notes=None):
        self.value = value
        self.user = user
        self.notes = notes
        self.valid_days = valid_days

        if expire_date is None and valid_days is not None:
            self.set_expire_date(valid_days)

    def set_expire_date(self, valid_days):
        # Calculate and set the expiration date based on the valid days
        self.expire_date = self.create_date + timedelta(days=valid_days)


class UserTokenRelationship(Base):
    __tablename__ = 'account_token_relationship'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.uid'), nullable=False)
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'), nullable=False)

    def __init__(self, user_id, token_id):
        self.user_id = user_id
        self.token_id = token_id
