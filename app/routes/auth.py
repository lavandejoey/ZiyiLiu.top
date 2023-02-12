#!/usr/bin/env python
# auth.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from flask import Blueprint, render_template
# local source

# local source
bp = Blueprint('auth', __name__, template_folder="templates")


@bp.route('/auth')
def index():
    return render_template('auth/sign.html')
