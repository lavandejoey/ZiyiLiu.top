#!/usr/bin/env python
# apis/jwt.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
from datetime import datetime, timedelta

# 3rd party packages
import jwt
from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required, create_access_token

# local source
from MainApplication.extentions import limiter
from .base import apis_blueprint, preprocess_request


@apis_blueprint.route("/jwt")
@jwt_required(optional=True)
@limiter.limit("1 per second")
def jwt_parse() -> jsonify:
    """
    Parse jwt token from header or cookie into dict, and check if it is valid.
    :argument: jwt token from header or cookie
    :return: jwt dict, 200 if valid, 400 if invalid
    """
    # Get jwt from header or cookie
    jwt_token = request.headers.get("Authorization").replace("Bearer ", "") if request.headers.get(
        "Authorization") else None
    jwt_token = request.cookies.get("access_token") if not jwt_token else jwt_token

    # No jwt found
    if not jwt_token:
        return jsonify({"status": "failed", "message": "no jwt found"}), 400

    # Parse jwt into dict and jsonify
    jwt_dict = jwt.decode(jwt_token, current_app.config["SECRET_KEY"],
                          algorithms=current_app.config["JWT_ALGORITHM"])
    # Check if jwt expired or not fresh
    # show validation(boolean), remaining time, until when
    # Check if jwt has an expiration time
    if "exp" in jwt_dict.keys():
        jwt_validation = datetime.fromtimestamp(jwt_dict["exp"]) > datetime.now()
        jwt_remains = datetime.fromtimestamp(jwt_dict["exp"]) - datetime.now()
        jwt_until = datetime.fromtimestamp(jwt_dict["exp"])

        return jsonify({"status": "success", "message": "jwt token parsed", "jwt": jwt_dict,
                        "valid": jwt_validation, "remaining": str(jwt_remains), "until": str(jwt_until)}), 200
    # Check if jwt is a fresh token
    elif "fresh" in jwt_dict.keys():
        jwt_validation = jwt_dict["fresh"]
        return jsonify(
            {"status": "success", "message": "jwt token parsed", "jwt": jwt_dict, "valid": jwt_validation}), 200
    else:
        # Token without an expiration time or freshness
        return jsonify({"status": "success", "message": "jwt token parsed", "jwt": jwt_dict, "valid": "unknown"}), 200


@apis_blueprint.route("/jwt/create", methods=["GET"])
def jwt_creation() -> jsonify:
    """
    Create a jwt token with given parameters.
    :argument: identity (opt) A string or object representing the identity of the user.
    :argument: fresh (opt) If true, create a fresh token that can be used for fresh login.
    :argument: expiration_param (opt) The expiration time of the token. Can either be a datetime or timedelta
    :argument: additional_claims (opt) Additional claims to include in the JWT payload.
    :return: jwt token, 200
    """
    # Get parameters from request
    request_params = preprocess_request()

    # Set default values
    identity = request_params.get("identity", None)
    fresh = request_params.get("fresh", False)

    # Extract additional claims
    additional_claims = {key: value for key, value in request_params.items()
                         if key not in ["identity", "fresh", "expiration_param"]}
    additional_claims["group"] = "user" if "group" not in additional_claims.keys() else additional_claims["group"]

    # Parse expiration parameter
    if request_params.get("expiration_param"):
        expiration_param = request_params.get("expiration_param")
        try:
            # Try to parse as datetime
            expires_at = datetime.fromisoformat(str(expiration_param))
            expires_delta = expires_at - datetime.utcnow()
        except ValueError or TypeError:
            # If parsing as datetime fails, treat as duration in seconds
            expires_delta = timedelta(seconds=int(str(expiration_param)))
    else:
        expires_delta = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]

    # Create a new jwt
    raw_jwt = create_access_token(identity=identity, fresh=fresh, expires_delta=expires_delta,
                                  additional_claims=additional_claims)

    # Additional information for response
    jwt_params = jwt.decode(raw_jwt, current_app.config["SECRET_KEY"], algorithms=current_app.config["JWT_ALGORITHM"])
    jwt_params.update({
        "created": datetime.fromtimestamp(jwt_params["iat"]).strftime("%Y-%m-%d %H:%M:%S"),
        "until": datetime.fromtimestamp(jwt_params["exp"]).strftime("%Y-%m-%d %H:%M:%S"),
        "remaining": str(datetime.fromtimestamp(jwt_params["exp"]) - datetime.now()).split(".")[0]
    })

    return jsonify({"status": "success", "message": "jwt token created", "jwt": raw_jwt, "jwt_params": jwt_params}), 200
