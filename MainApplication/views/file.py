#!/usr/bin/env python
# file.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from flask import Blueprint, abort, request, send_from_directory

# local source

file_blueprint = Blueprint(name="file", import_name=__name__, static_folder="static", static_url_path="/static",
                           template_folder="templates", url_prefix="/static", subdomain=None, url_defaults=None,
                           cli_group=None)


# Custom route handler for serving static files
@file_blueprint.route('/static/<path:filename>', methods=['GET'])
def serve_static_file(filename):
    # Check if the request originated from the server
    if request.remote_addr != '127.0.0.1':
        # Return a 403 error if the request is not from the server
        abort(403)
    # If the request is from the server, serve the static file
    return send_from_directory(file_blueprint.static_folder, filename)
