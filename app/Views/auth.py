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
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user,logout_user,login_required
# local source
from app import db
from app.APIs import str_hash, str_verify
from app.Models import Users

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth', url_prefix="/auth")


@auth_bp.route('/')
@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')


@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(usr_email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not str_verify(hashed_passwd=user.usr_pw_hash, raw_passwd=password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth_bp.route('/signup')
def signup():
    return render_template('auth/signup.html')


@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    print("form:", email, name, password)
    # if this returns a user, then the email already exists in database
    check_username = Users.query.filter_by(usr_name=name).first()
    print(f"exist:{check_username}")
    check_email = Users.query.filter_by(usr_email=email).first()
    print(check_email)
    if check_username or check_email:  # if a user is existed, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = Users(usr_email=email, usr_name=name, usr_pw_hash=str_hash(password))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
