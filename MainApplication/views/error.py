#!/usr/bin/env python
# errors.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from flask import Blueprint

# local source

error_blueprint = Blueprint(name="error", import_name=__name__, static_folder="static", static_url_path="/static",
                            template_folder="templates", url_prefix="/error", subdomain=None, url_defaults=None,
                            cli_group=None)


@error_blueprint.app_errorhandler(404)
def not_found(error):
    return "404"


@error_blueprint.app_errorhandler(400)
def bad_request(error):
    return "400"


@error_blueprint.app_errorhandler(403)
def forbidden(error):
    return "403"


@error_blueprint.app_errorhandler(405)
def method_not_allowed(error):
    return "405"


@error_blueprint.app_errorhandler(500)
def internal_error(error):
    return "500"


@error_blueprint.app_errorhandler(501)
def not_implemented(error):
    return "501"


@error_blueprint.app_errorhandler(502)
def bad_gateway(error):
    return "502"
