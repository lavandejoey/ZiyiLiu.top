#!/usr/bin/env python
# apis/repos.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
import re
from datetime import datetime

# 3rd party packages
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token

# local source
from MainApplication.models import User
from .base import apis_blueprint, preprocess_request


# User existence
@apis_blueprint.route("/db/user-exist", methods=["GET"])
def db_user_exist():
    # Parse arg
    request_params = preprocess_request()
    uid = request_params.get("uid").replace("\"", "") if request_params.get("uid") else None
    username = request_params.get("username").replace("\"", "") if request_params.get("username") else None
    email = request_params.get("email").replace("\"", "") if request_params.get("email") else None
    # Enquiry the user intersection list of uid, username, email
    try:
        users_list = [user.to_dict(with_groups=True) for user in User.query.filter(
            # remove 0 at start
            User.uid == re.sub(r"^0+", "", uid) if uid else True,
            User.username == username if username else True,
            User.email == email if email else True).all()]
        if len(users_list) == 0:
            results = {"status": "failed",
                       "message": "no user found",
                       "exists": False}
        else:
            results = {"status": "success",
                       "message": f"{len(users_list)} user(s) found",
                       "exists": True,
                       "count": len(users_list),
                       "users": users_list}
    except Exception as e:
        results = {"status": "failed",
                   "message": f"error: {e}"}
    return jsonify(results), 200


# User inquiry and update
@apis_blueprint.route("/db/user", methods=["GET", "POST"])
@jwt_required()
def db_user():
    # Parse arg
    request_params = preprocess_request()
    uid = request_params.get("uid").replace("\"", "") if request_params.get("uid") else None
    username = request_params.get("username").replace("\"", "") if request_params.get("username") else None
    email = request_params.get("email").replace("\"", "") if request_params.get("email") else None
    password = request_params.get("password").replace("\"", "") if request_params.get("password") else None
    # GET
    if request.method == "GET":
        # Enquiry the user intersection list of uid, username, email
        users_list = [user.to_dict(with_groups=True) for user in User.query.filter(
            # remove 0 at start
            User.uid == re.sub(r"^0+", "", uid) if uid else True,
            User.username == username if username else True,
            User.email == email if email else True).all()]
        if len(users_list) == 0:
            return jsonify({"status": "failed", "message": "no user found"}), 404
        else:
            return jsonify({"status": "success", "message": f"{len(users_list)} user(s) found",
                            "count": len(users_list), "users": users_list}), 200
    # POST:
    if request.method == "POST":
        # Enquiry the user intersection list of uid, username, email
        user = User.query.filter(
            User.uid == re.sub(r"^0+", "", uid) if uid else True,
            User.username == username if username else True,
            User.email == email if email else True).first()
        if user:
            user.username = username if username else user.username
            user.email = email if email else user.email
            user.set_password(password) if password else None
            user.updated_at = datetime.now()
            user.add_commit()
            return jsonify(
                {"status": "success", "message": f"Update user {user.uid} successful", "user": user.to_dict()}), 200
        else:
            return jsonify({"status": "failed", "message": "No user found"}), 404


# PUT create a new one
@apis_blueprint.route("/db/user", methods=["PUT"])
def db_user_add():
    # Parse body
    uid = request.json.get("uid").replace("\"", "") if request.json.get("uid") else None
    username = request.json.get("username").replace("\"", "") if request.json.get("username") else None
    email = request.json.get("email").replace("\"", "") if request.json.get("email") else None
    password = request.json.get("password").replace("\"", "") if request.json.get("password") else None
    # Enquiry the user intersection list of uid, username, email
    user = User.query.filter(
        User.username == username if username else True,
        User.email == email if email else True).first()
    if user:
        return jsonify({"status": "failed", "message": "User already exist"}), 409
    else:
        phone = request.json.get("phone").replace("\"", "") if request.json.get("phone") else None
        user = User(username=username, email=email, phone=phone)
        user.set_password(password) if password else None
        user.created_at, user.updated_at = datetime.now(), datetime.now()
        user.add_commit()
        return jsonify({"status": "success", "message": f"Create user {user.uid} successful",
                        "user": user.to_dict()}), 200


# User inquiry
@apis_blueprint.route("/db/user-count", methods=["GET"])
def db_user_count():
    user_count = User.query.count()
    return jsonify({"status": "success", "message": f"{user_count} user(s) found",
                    "count": user_count}), 200


@apis_blueprint.route("/db/auth", methods=["POST"])
def db_auth():
    # Parse args
    username = request.json.get("username").replace("\"", "") if request.json.get("username") else None
    email = request.json.get("email").replace("\"", "") if request.json.get("email") else None
    user = User.query.filter(
        User.username == username if username else True,
        User.email == email if email else True).first()
    password = request.json.get("password").replace("\"", "") if request.json.get("password") else None
    with_token = True if request.json.get("with_token") else False
    # Enquiry username and email
    if user:
        if user.check_password(password):
            if with_token:
                token = create_access_token(identity=user.to_dict()["username"])
                return jsonify({"status": "success", "message": "Login successful",
                                "user": user.to_dict(), "jwt": token}), 200
            return jsonify({"status": "success", "message": "Login successful", "user": user.to_dict()}), 200
        else:
            return jsonify({"status": "failed", "message": "Credential error"}), 401
    else:
        return jsonify({"status": "failed", "message": "No user found"}), 404
