#!/usr/bin/env python
# main.py
"""The main pages that deploy personal portfolio and link with the other main_bp"""
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import current_user
from flask_mail import Message, Mail
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

# local source
from app.Forms import *

mail = Mail()

main_bp = Blueprint('main', __name__, template_folder="templates", url_prefix="/")


@main_bp.route('/')
def temp():
    return render_template('tmp/index_tmp.html')


@main_bp.route('/index')
@main_bp.route('/home')
def index():
    code = '''
    @main_bp.route("/")
    def hello():
        code = """
        def hello():
            print("Hello, World!")
        """
        highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())
        return render_template("index.html", highlighted_code=highlighted_code)
    '''
    style = get_style_by_name("nord-darker")
    formatter = HtmlFormatter(style=style, linenos='inline', title="", linenostart=0, linenostep=2,
                              nobackground=False, noclasses=True)
    highlighted_code = highlight(code, PythonLexer(), formatter)
    return render_template('main/index.html', code=highlighted_code)


@main_bp.route('/blog')
def blog():
    return render_template('main/blog.html')


@main_bp.route('/work')
def work():
    return render_template('main/blog.html')  # TODO!:the work display page


@main_bp.route('/about')
def about():
    return render_template('main/about.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(subject='Lzyatshcn.top Contact Form Submission',
                      recipients=['lavandejoey@outlook.com'],
                      sender=form.email.data)
        msg.body = f"Name: {form.name.data}\n\nEmail: {form.email.data}\n\nMessage: {form.message.data}"
        mail.send(msg)
        flash('Your message has been sent!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html', form=form)


@main_bp.route('/profile')
def profile():
    return render_template('main/profile.html', name=current_user.usr_name)
