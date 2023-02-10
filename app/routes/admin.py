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
from app.models.admin import *

admin_bp = Blueprint('admin', __name__, template_folder='templates/admin', url_prefix="/admin")


@admin_bp.route('/login')
def login():
    return render_template('admin/admin_login.html', title="Welcome")


@admin_bp.route('/dashboard')
def dashboard():
    user_list = users.query.all()
    return render_template('admin/dashboard.html', user_list=user_list)


@admin_bp.route('/api_manage')
def api_manage():
    return render_template('admin/api_manage.html', title="APIs")
