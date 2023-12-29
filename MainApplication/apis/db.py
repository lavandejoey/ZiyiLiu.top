#!/usr/bin/env python
# apis/repos.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
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
from .base import apis_blueprint


# User existence
@apis_blueprint.route("/db/user-exist", methods=["GET"])
def db_user_exist():
    # Parse arg
    uid = request.args.get("uid").replace("\"", "") if request.args.get("uid") else None
    username = request.args.get("username").replace("\"", "") if request.args.get("username") else None
    email = request.args.get("email").replace("\"", "") if request.args.get("email") else None
    # Enquiry the user intersection list of uid, username, email
    users_list = [user.to_dict(with_groups=True) for user in User.query.filter(
        # remove 0 at start
        User.uid == re.sub(r"^0+", "", uid) if uid else True,
        User.username == username if username else True,
        User.email == email if email else True).all()]
    if len(users_list) == 0:
        return jsonify({"status": "failed", "msg": "no user found", "exists": False}), 404
    else:
        return jsonify({"status": "success", "msg": f"{len(users_list)} user(s) found", "exists": True,
                        "count": len(users_list), "users": users_list}), 200


# User inquiry and update
@apis_blueprint.route("/db/user", methods=["GET", "POST"])
@jwt_required()
def db_user():
    # GET
    if request.method == "GET":
        # Parse arg
        uid = request.args.get("uid").replace("\"", "") if request.args.get("uid") else None
        username = request.args.get("username").replace("\"", "") if request.args.get("username") else None
        email = request.args.get("email").replace("\"", "") if request.args.get("email") else None
        # Enquiry the user intersection list of uid, username, email
        users_list = [user.to_dict(with_groups=True) for user in User.query.filter(
            # remove 0 at start
            User.uid == re.sub(r"^0+", "", uid) if uid else True,
            User.username == username if username else True,
            User.email == email if email else True).all()]
        if len(users_list) == 0:
            return jsonify({"status": "failed", "msg": "no user found"}), 404
        else:
            return jsonify({"status": "success", "msg": f"{len(users_list)} user(s) found",
                            "count": len(users_list), "users": users_list}), 200
    # Parse body
    uid = request.json.get("uid").replace("\"", "") if request.json.get("uid") else None
    username = request.json.get("username").replace("\"", "") if request.json.get("username") else None
    email = request.json.get("email").replace("\"", "") if request.json.get("email") else None
    password = request.json.get("password").replace("\"", "") if request.json.get("password") else None
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
                {"status": "success", "msg": f"Update user {user.uid} successful", "user": user.to_dict()}), 200
        else:
            return jsonify({"status": "failed", "msg": "No user found"}), 404

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
        return jsonify({"status": "failed", "msg": "User already exist"}), 409
    else:
        phone = request.json.get("phone").replace("\"", "") if request.json.get("phone") else None
        user = User(username=username, email=email, phone=phone)
        user.set_password(password) if password else None
        user.created_at, user.updated_at = datetime.now(), datetime.now()
        user.add_commit()
        return jsonify({"status": "success", "msg": f"Create user {user.uid} successful",
                        "user": user.to_dict()}), 200


# User inquiry
@apis_blueprint.route("/db/user-count", methods=["GET"])
def db_user_count():
    user_count = User.query.count()
    return jsonify({"status": "success", "msg": f"{user_count} user(s) found",
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
                return jsonify({"status": "success", "msg": "Login successful",
                                "user": user.to_dict(), "jwt": token}), 200
            return jsonify({"status": "success", "msg": "Login successful", "user": user.to_dict()}), 200
        else:
            return jsonify({"status": "failed", "msg": "Credential error"}), 401
    else:
        return jsonify({"status": "failed", "msg": "No user found"}), 404

# # Access test
# @apis_blueprint.route("/get_jwt_user")
# @jwt_required()
# def jwt_user():
#     # verify_jwt_in_request:
#     # Check if a valid JWT is present in the request.
#     if not request.headers.get('Authorization'):
#         return jsonify({
#             'status': 'failed',
#             'cookie': request.cookies,
#             'msg': 'missing Authorization header'}), 401
#     else:
#         from flask_jwt_extended import verify_jwt_in_request
#         verify_jwt_in_request()
#
#     current_user = get_jwt_identity()
#     print(current_user)
#     return jsonify({
#         'user': current_user,
#         'status': 'success',
#         'cookie': request.cookies,
#         'msg': 'jwt test success'}), 200


# @apis_blueprint.route('/get_test_token')
# def jwt_test_token():
#     jtw_token = create_access_token(identity='test')
#     try:
#         # parsing token info
#         import jwt
#         decoded_token = jwt.decode(jtw_token, key=current_app.config.get('JWT_SECRET_KEY'),
#                                    identity='test', algorithms=["HS256"])
#         msg = 'jwt token parse success'
#     except:
#         decoded_token = ''
#         msg = 'jwt token parse failed'
#
#     headers = {'Authorization': 'Bearer ' + jtw_token}
#     # get dict from api.jwt_user()
#     jwt_user_response = requests.get(url_for('apis.jwt_user', _external=True), headers=headers)
#     rsp = jwt_user_response.json()
#     # get jwt_user_response request param
#
#     return jsonify({
#         'status': 'success',
#         'token': jtw_token,
#         'decoded_token': decoded_token,
#         'jwt_user': rsp,
#         # "jwt_header": jwt_header,
#         'msg': msg}), 200
