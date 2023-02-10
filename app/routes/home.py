#!/usr/bin/env python
# home.py
"""The main pages that deploy personal portfolio and link with the other home_bp"""
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
home_bp = Blueprint('home', __name__, template_folder="templates")


@home_bp.route('/')
def index():
    return render_template('home/index.html')


@home_bp.route('/blog')
def blog():
    return render_template('home/blog.html')


@home_bp.route('/about')
def about():
    return render_template('home/about.html')


@home_bp.route('/contact')
def contact():
    return render_template('home/contact.html')
