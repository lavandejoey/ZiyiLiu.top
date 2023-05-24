#!/usr/bin/env python
# forms/email.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    message = TextAreaField('message', validators=[DataRequired()])

    def format(self):
        return f"Name: {self.name.data}\n\nEmail: {self.email.data}\n\nMessage: {self.message.data}"
