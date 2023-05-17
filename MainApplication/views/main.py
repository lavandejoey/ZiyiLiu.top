#!/usr/bin/env python
# main.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from flask import Blueprint, render_template, flash
from flask_mail import Message, Mail

# local source
from MainApplication.forms import ContactForm

mail = Mail()

main_blueprint = Blueprint(name="main", import_name=__name__, static_folder="static", static_url_path="/static",
                           template_folder="templates", url_prefix="/", subdomain=None, url_defaults=None,
                           root_path="/media/lavandejoey/Documents/CODE/PROJECTS/JoshuaZiyiLiu/MainApplication",
                           cli_group=None)


# The index page of the main application
@main_blueprint.route('/index')
@main_blueprint.route('/main')
@main_blueprint.route('/home')
@main_blueprint.route('/')
def index_page():
    return render_template("index.html", title="Joshua Ziyi Liu", page="index")


# Curriculum Vitae
@main_blueprint.route('/cv')
def cv_page():
    return render_template("cv.html", title="Curriculum Vitae", page="cv")


# Contact me page
@main_blueprint.route('contact', methods=['GET', 'POST'])
def contact_page():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        msg = Message(subject='JoshuaZiyiLiu.com Contact Form Submission',
                      recipients=[__email__],
                      sender=contact_form.email.data)
        msg.body = f"Name: {contact_form.name.data}\n\nEmail: {contact_form.email.data}\n\nMessage: {contact_form.message.data}"
        mail.send(msg)
        flash('Your message has been sent!', 'success')
        return render_template("contact.html", title="Contact Me", page="contact")
    return render_template("contact.html", title="Contact Me", page="contact", form=contact_form)
