#!/usr/bin/env python
# apis/base.py
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

apis_blueprint = Blueprint(name="apis", import_name=__name__, url_prefix="/api")
