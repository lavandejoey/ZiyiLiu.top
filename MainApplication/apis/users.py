#!/usr/bin/env python
# apis/users.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library

# 3rd party packages
from flask import jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import or_

from MainApplication.extentions import limiter
# local source
from MainApplication.models import User
from .base import apis_blueprint, preprocess_request


@apis_blueprint.route("/users", methods=["GET"])
@jwt_required()
@limiter.limit("1 per second")
def get_all_users() -> jsonify:
    """
    The function allows admin user to retrieve all users' info.
    :return: The dict of all users
    """
    # Check if the user has admin privileges
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user_id and current_user.is_admin():
        # Retrieve all users' information
        users = User.query.all()
        user_info = [user.to_dict(with_groups=True) for user in users]
        return jsonify({"status": "success", "message": "All users retrieved", "users": user_info}), 200
    else:
        return jsonify({"status": "failed", "message": "Unauthorized access"}), 401


@apis_blueprint.route("/user", methods=["GET"])
@apis_blueprint.route("/user/<string:uid>", methods=["GET"])
@jwt_required()
@limiter.limit("1 per second")
def get_single_user(uid=None) -> jsonify:
    """
    The function is used to retrieve certain user's info.
    Allowing admin user to retrieve any user's info, and allowing user to retrieve its own info.
    Enquiry the user intersection list of uid, username, email
    :param uid: The uid is optional, if not provided, the uid will be retrieved from request parameters
    :return:
    """
    # Get parameters from request
    request_params = preprocess_request()

    # Use uid from URL if available, otherwise use uid from request_params
    uid = uid or request_params.get("uid", "").replace("\"", "")
    username = request_params.get("username", "").replace("\"", "")

    # Check if the current user has admin privileges or is the requested user
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user and (current_user.is_admin() or current_user.uid == uid):
        # Retrieve single user's information
        user = User.query.filter(or_(User.uid == uid, User.username == username)).first()
        if user:
            user_info = user.to_dict(with_groups=True)
            return jsonify({"status": "success", "message": "User information retrieved", "user": user_info}), 200
        else:
            return jsonify({"status": "failed", "message": "User not found"}), 404
    else:
        return jsonify({"status": "failed", "message": "Unauthorized access"}), 401


@apis_blueprint.route("/user", methods=["PUT"])
@jwt_required()
@limiter.limit("1 per second")
def update_user_info() -> jsonify:
    """
    The function is used to update certain user's info.
    Allowing admin user to update any user's info, and allowing user to update its own info.
    :return: The dict of the updated user
    """
    # Get parameters from request
    request_params = preprocess_request()
    uid = request_params.get("uid").replace("\"", "") if request_params.get("uid") else None
    username = request_params.get("username").replace("\"", "") if request_params.get("username") else None

    # Check if the current user has admin privileges or is the requested user
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user and (current_user.is_admin() or current_user.uid == uid):
        # Update user's information
        user = User.query.filter(or_(User.uid == uid, User.username == username)).first()
        if user:
            # Update user's information based on request parameters
            user.username = request_params.get("new_username", user.username)
            user.email = request_params.get("new_email", user.email)
            user.phone = request_params.get("new_phone", user.phone)

            user.add_commit()

            user_info = user.to_dict(with_groups=True)
            return jsonify({"status": "success", "message": "User information updated", "user": user_info}), 200
        else:
            return jsonify({"status": "failed", "message": "User not found"}), 404
    else:
        return jsonify({"status": "failed", "message": "Unauthorized access"}), 401


@apis_blueprint.route("/user", methods=["DELETE"])
@jwt_required()
@limiter.limit("1 per second")
def delete_user() -> jsonify:
    """
    This function is used to delete a user from the database.
    Only admin users or the user itself can delete the user.
    :return: The dict of the deleted user
    """
    # Get parameters from request
    request_params = preprocess_request()
    uid = request_params.get("uid").replace("\"", "") if request_params.get("uid") else None
    username = request_params.get("username").replace("\"", "") if request_params.get("username") else None

    # Check if the current user has admin privileges or is the requested user
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user and (current_user.is_admin() or current_user.uid == uid):
        # Delete user
        user = User.query.filter(or_(User.uid == uid, User.username == username)).first()
        if user:
            user.delete()
            return jsonify({"status": "success", "message": "User deleted"}), 200
        else:
            return jsonify({"status": "failed", "message": "User not found"}), 404
    else:
        return jsonify({"status": "failed", "message": "Unauthorized access"}), 401


@apis_blueprint.route("/user", methods=["POST"])
@limiter.limit("1 per second")
def create_user() -> jsonify:
    """
    This function is used to create a new user.
    :return:
    """
    # Get parameters from request
    request_params = preprocess_request()
    username = request_params.get("username").replace("\"", "") if request_params.get("username") else None
    email = request_params.get("email").replace("\"", "") if request_params.get("email") else None
    phone = request_params.get("phone").replace("\"", "") if request_params.get("phone") else None
    password = request_params.get("password").replace("\"", "") if request_params.get("password") else None

    # Create user
    new_user = User(username=username, email=email, phone=phone)
    new_user.set_password(password)
    new_user.add_commit()

    user_info = new_user.to_dict(with_groups=True)
    return jsonify({"status": "success", "message": "User created", "user": user_info}), 201


@apis_blueprint.route("/user/authentication", methods=["POST"])
@limiter.limit("1 per second")
def user_authentication():
    # Get parameters from request
    request_params = preprocess_request()
    username = request_params.get("username").replace("\"", "") if request_params.get("username") else None
    email = request_params.get("email").replace("\"", "") if request_params.get("email") else None
    password = request_params.get("password").replace("\"", "") if request_params.get("password") else None
    with_token = True if request_params.get("with_token") else False

    # If not input username or email, or not input password
    if (not username and not email) or not password:
        return jsonify({"status": "failed", "message": "Missing credential"}), 400

    # Authenticate user
    user = User.query.filter(
        User.username == username if username else True,
        User.email == email if email else True).first()

    if user and user.check_password(password):
        if with_token:
            token = create_access_token(identity=user.to_dict()["username"], fresh=True)
            return jsonify({"status": "success", "message": "Login successful",
                            "user": user.to_dict(), "jwt": token}), 200
        return jsonify({"status": "success", "message": "Login successful", "user": user.to_dict()}), 200
    else:
        return jsonify({"status": "failed", "message": "Credential error"}), 401
