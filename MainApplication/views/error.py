#!/usr/bin/env python
# views/error.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from flask import Blueprint, render_template
from flask_babel import gettext

# local source

error_blueprint = Blueprint(name="error", import_name=__name__, static_folder="static", static_url_path="/static",
                            template_folder="templates", subdomain=None, url_defaults=None,
                            cli_group=None)


@error_blueprint.app_errorhandler(400)  # 400 Bad Request
@error_blueprint.app_errorhandler(403)  # 403 Forbidden
@error_blueprint.app_errorhandler(404)  # 404 Not Found
@error_blueprint.app_errorhandler(405)  # 405 Method Not Allowed
def handle_error(error):
    return render_template('error/error.html',
                           title=gettext("Error"),
                           error_code=error.code,
                           error_name=error.name), error.code


@error_blueprint.app_errorhandler(500)
def internal_error(error):
    return render_template('error/error.html',
                           title=gettext("Internal Server Error"),
                           error_code=error.code,
                           error_name=error.name), error.code


@error_blueprint.app_errorhandler(501)
def not_implemented(error):
    return render_template('error/error.html',
                           title=gettext("Not Implemented"),
                           error_code=error.code,
                           error_name=error.name), error.code


@error_blueprint.app_errorhandler(502)
def bad_gateway(error):
    return render_template('error/error.html',
                           title=gettext("Bad Gateway"),
                           error_code=error.code,
                           error_name=error.name), error.code
