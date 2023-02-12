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
from flask import request, jsonify

# local source
from app.APIs import hash_argon
from app.Models.admin import *
from app.Views.admin import admin_bp


@admin_bp.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    username_or_email = data.get("username_or_email")
    password = data.get("password")

    user = Users.query.filter(or_(Users.usr_name == username_or_email, Users.usr_email == username_or_email)).first()

    if not user:
        return jsonify({'message': 'Login successful'}), 400

    elif not hash_argon.str_verify(hashed_passwd=user.usr_pw_hash, raw_passwd=password):
        return jsonify({"error": "Incorrect password"}), 400

    else:
        return jsonify({"error": "Incorrect password"}), 400
