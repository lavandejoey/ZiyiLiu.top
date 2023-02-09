#!/usr/bin/env python
# admin.py
"""Web site management background"""
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

bp = Blueprint('admin', __name__, template_folder='templates/admin',prefix="/admin")


@bp.route('/test')
def test():
    return render_template('admin/test.html', title="Test")

@bp.route('/login')
def login():
    return render_template('admin/admin_login.html', title="Welcome")

@bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html', title="Dashboard")

@bp.route('/api_manage')
def test():
    return render_template('admin/api_manage.html', title="APIs")
