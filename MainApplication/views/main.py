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
from flask import Blueprint, render_template, flash, request, current_app
from flask_mail import Message

# local source
from MainApplication.forms import ContactForm

main_blueprint = Blueprint(name="main", import_name=__name__, static_folder="static", static_url_path="/static",
                           template_folder="templates", url_prefix="/", subdomain=None, url_defaults=None,
                           cli_group=None)


# The index page of the main application
@main_blueprint.route('/index')
@main_blueprint.route('/main')
@main_blueprint.route('/home')
@main_blueprint.route('/')
def index_page():
    return render_template("main/index.html", title="Joshua Ziyi Liu", page="index")


@main_blueprint.route('/portfolio')
def portfolio_page():
    return render_template("main/portfolio.html", title="Portfolio", page="portfolio")


# Curriculum Vitae
@main_blueprint.route('/cv')
def cv_page():
    return render_template("main/cv.html", title="Curriculum Vitae", page="cv")


# Contact me page
@main_blueprint.route('/contact', methods=['GET', 'POST'])
def contact_page():
    contact_form = ContactForm()
    csrf_token = request.form.get('csrf_token')
    if request.method == 'GET':
        return render_template("main/contact.html", title="Contact Me", page="contact", form=contact_form,
                               msg_sent=False)
    elif request.method == 'POST' and contact_form.validate_on_submit():
        # send email
        msg = Message(subject='JoshuaZiyiLiu.com Contact Form Submission',
                      recipients=[current_app.config["MAIL_DEFAULT_RECIPIENT"], ],
                      body=contact_form.format(),
                      charset="utf-8",
                      extra_headers={"X-CSRFToken": csrf_token},
                      reply_to=contact_form.email.data)
        current_app.extensions['mail'].send(msg)
        contact_form = ContactForm()
        return render_template("main/contact.html", title="Contact Me", page="contact", form=contact_form,
                               msg_sent=True)
    else:
        flash("Please check your input.")
        return render_template("main/contact.html", title="Contact Me", page="contact", form=contact_form,
                               msg_sent=False)
