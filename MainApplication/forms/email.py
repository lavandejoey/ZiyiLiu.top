#!/usr/bin/env python
# email.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField


class ContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    message = TextAreaField('message', validators=[DataRequired()])
