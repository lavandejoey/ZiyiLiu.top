#!/usr/bin/env python
# models/auth.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

from datetime import datetime, timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_login import UserMixin

from .base import *

ph = PasswordHasher()


class User(Base, UserMixin):
    """
    User model to store user information.
    """
    __tablename__ = 'accounts'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(32))
    # country_code = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, username, email, phone=None):
        self.username = username
        self.email = email
        self.phone = phone

    def to_dict(self, with_groups: bool = False) -> dict:
        """
        Convert user information to a dictionary.
        """
        if with_groups:
            user_groups = self.get_user_groups()
            return {'uid': self.get_id(), 'username': self.username, 'email': self.email, 'phone': self.phone,
                    'groups': user_groups, 'created_at': self.created_at, 'updated_at': self.updated_at}
        else:
            return {'uid': self.get_id(), 'username': self.username, 'email': self.email, 'phone': self.phone,
                    'created_at': self.created_at, 'updated_at': self.updated_at}

    # cannot be used out of class private methods
    @staticmethod
    def hash_password(password) -> str:
        """
        Hash the provided password using PBKDF2.
        """
        return ph.hash(password)

    def set_password(self, password) -> None:
        """
        Set the password for the user.
        """
        self.password = self.hash_password(password)

    def check_password(self, password) -> bool:
        """
        Verify the provided password against the stored hash.
        """
        try:
            return ph.verify(self.password, password)
        except VerifyMismatchError:
            return False

    def get_id(self) -> str:
        """
        Get the formatted user ID.
        """
        return f"{self.uid:08d}"

    def get_user_groups(self) -> list:
        """
        Get the groups that the user belongs to.
        """
        group_relationships = db.session.query(UserGroupRelationship).filter(
            UserGroupRelationship.account_id == self.uid).all()

        groups = []
        for group_relationship in group_relationships:
            group = db.session.query(Group).filter(Group.group_id == group_relationship.group_id).first()
            groups.append({
                'id': group.group_id,
                'name': group.group_name
            })

        return sorted(groups, key=lambda k: k['id'])

    def belong_to_group(self, g_id: int = None, g_name: str = None) -> bool:
        """
        Check if the user belongs to a specific group.
        """
        if not g_id and not g_name:
            raise ValueError("Either g_id or g_name must be provided")

        if g_id:
            return db.session.query(UserGroupRelationship).filter(
                UserGroupRelationship.account_id == self.uid,
                UserGroupRelationship.group_id == g_id).first() is not None

        if g_name:
            group = db.session.query(Group).filter(Group.group_name == g_name).first()
            if not group:
                raise ValueError(f"Group {g_name} does not exist")
            return db.session.query(UserGroupRelationship).filter(
                UserGroupRelationship.account_id == self.uid,
                UserGroupRelationship.group_id == group.group_id).first() is not None

        return False

    def is_admin(self) -> bool:
        """
        Check if the user is an administrator.
        """
        return self.belong_to_group(g_name="administrator")


class Group(Base):
    """
    Group model to store groups for users.
    """
    __tablename__ = 'groups'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(64), nullable=False)

    def __init__(self, group_name):
        """
        Initialize a new Group instance.
        :param group_name: The name of the group.
        """
        self.group_name = group_name


class UserGroupRelationship(Base):
    """
    UserGroupRelationship model to store the relationship between users and groups.
    """
    __tablename__ = 'account_group_relationship'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.uid'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)

    def __init__(self, account_id, group_id):
        """
        Initialize a new UserGroupRelationship instance.
        :param account_id: The ID of the user.
        :param group_id: The ID of the group.
        """
        self.account_id = account_id
        self.group_id = group_id


class Token(Base):
    """
    Token model to store authentication tokens for users.
    """
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    valid_days = db.Column(db.Integer, nullable=False)

    def __init__(self, user, expire_date=None, valid_days=None, notes=None):
        """
        Initialize a new Token instance.
        :param user: User object to associate the token with.
        :param expire_date: Optional expiration date for the token.
        :param valid_days: Optional number of valid days for the token.
        :param notes: Optional notes for the token.
        """
        self.user = user
        self.notes = notes
        self.valid_days = valid_days

        if expire_date is None and valid_days is not None:
            self.set_expire_date(valid_days)

    def set_expire_date(self, valid_days) -> None:
        """
        Calculate and set the expiration date based on the valid days.
        :param valid_days: Number of valid days for the token.
        :return None
        """
        # Calculate and set the expiration date based on the valid days
        self.expire_date = self.create_date + timedelta(days=valid_days)


class UserTokenRelationship(Base):
    __tablename__ = 'user_token_relationship'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.uid'))
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'))

    # Define relationships
    user = db.relationship('User', backref='token_relationships')
    token = db.relationship('Token', backref='user_relationships')
