#!/usr/bin/env python
# apis/base.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
import jwt
from flask import Blueprint, jsonify, request, current_app
# get_raw_jwt
from flask_jwt_extended import jwt_required, create_access_token

# local source

apis_blueprint = Blueprint(name="apis", import_name=__name__, static_folder="static", static_url_path="/static",
                           url_prefix="/r", subdomain=None)


def preprocess_request():
    """
    Preprocesses the API request to parse input parameters into a dict.
    :return: dict of parsed parameters
    """
    parsed_params = {}

    # Parse JSON data from request body
    if request.is_json:
        parsed_params.update(request.json)
    # Parse form data from request
    parsed_params.update(request.form)
    # Parse query parameters from URL
    parsed_params.update(request.args)
    # Parse route parameters
    parsed_params.update(request.view_args)

    return parsed_params


@apis_blueprint.route('/', methods=['GET'])
def welcome_api() -> jsonify:
    """
    Welcome API
    :return: welcome message, 200
    """
    welcome_message = {
        'status': 'success',
        'message': 'Welcome to Joshua\'s website APIs! Explore the endpoints to access different functionalities.',
        'api_version': 'v1.0',
        'author': 'Joshua LIU',
        'email': 'lavandejoey@outlook.com'
    }
    return jsonify(welcome_message), 200


@apis_blueprint.route('/test', methods=['GET'])
@jwt_required(optional=True)
def test_api() -> jsonify:
    """
    Test API, only available in debug mode.
    :return: test message, 200
    """
    # Check debug mode
    if not current_app.debug:
        return jsonify({"message": "This API is only available in debug mode."}), 403

    # Create a new jwt
    raw_jwt = create_access_token(
        identity="test_new",
        fresh=True,
        # expires_delta=True,
        additional_claims={"test": "test", "group": "test"},
        additional_headers={"header": "header"}
    )
    return jsonify({"new_jwt": raw_jwt,
                    "new_jwt_raw": jwt.decode(raw_jwt, current_app.config["SECRET_KEY"],
                                              algorithms=current_app.config["JWT_ALGORITHM"]),
                    # "in_jwt": get_jwt()
                    }), 200
    #
    # # Check if raw_jwt is present and not empty
    # if raw_jwt:
    #     return raw_jwt.get('identity', {})  # 'identity' is the default claim for user identity
    # else:
    #     return {'msg': 'No JWT present in request'}, 200
