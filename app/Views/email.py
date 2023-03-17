#!/usr/bin/env python
# emain.py
"""Blog and functional sections, controls user permissions to browse and use functions."""
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_mail import Message, Mail

# local source
from app.Forms import *

mail = Mail()

email_bp = Blueprint("email", __name__, template_folder="templates", url_prefix="/email")


@email_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(subject='Lzyatshcn.top Contact Form Submission',
                      recipients=[__email__],
                      sender=form.email.data)
        msg.body = f"Name: {form.name.data}\n\nEmail: {form.email.data}\n\nMessage: {form.message.data}"
        mail.send(msg)
        flash('Your message has been sent!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html', form=form)
