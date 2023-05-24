#!/usr/bin/env python
# game.py
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

game_blueprint = Blueprint(name="game", import_name=__name__, static_folder="static", static_url_path="/static",
                           template_folder="templates", url_prefix="/game", subdomain=None, url_defaults=None,
                           cli_group=None)
