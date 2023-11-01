#!/usr/bin/env python
# views/auth.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_babel import gettext
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_

# local source
from MainApplication.forms import LoginForm, SignupForm
from MainApplication.models import User, UserGroupRelationship

auth_blueprint = Blueprint(name="auth", import_name=__name__, static_folder="static", url_prefix="/auth",
                           template_folder="templates")


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('auth.user_page', uid=current_user.uid))

    form = LoginForm()
    user_not_found = False
    password_error = False

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Check if the user exists in the database by matching against username, email, or phone
        user = User.query.filter(or_(
            User.username == username,
            User.email == username,
            User.phone == username
        )).first()

        if user:
            if user.check_password(password):
                # Log the user in
                login_user(user)
                flash(gettext('Login successful'), 'success')
                # If next param exists, redirect to that page
                if 'next' in request.args:
                    return redirect(request.args.get('next'))
                else:
                    return redirect(url_for('auth.user_page', uid=user.uid))
            else:
                password_error = True
                flash(gettext('Incorrect password'), 'danger')
        else:
            user_not_found = True
            flash(gettext('User not found'), 'danger')

    return render_template('auth/login.html', title="Login", page="login",
                           form=form, user_not_found=user_not_found, password_error=password_error)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('auth.user_page', uid=current_user.uid))

    form = SignupForm()
    user_exists = False
    signup_finished = False

    if form.validate_on_submit():
        username, password, email, phone = form.username.data, form.password.data, form.email.data, form.phone.data
        existing_user = User.query.filter(or_(User.username == username)).first()
        existing_email = User.query.filter(or_(User.email == email)).first()

        if existing_user:
            user_exists = True
            flash(gettext('User already exists. Try a different one or log in.'), 'danger')
        elif existing_email:
            user_exists = True
            flash(gettext('Email already exists. Try a different one or log in.'), 'danger')
        else:
            user = User(username=username, email=email, phone=phone)
            user.set_password(password)
            user_group = UserGroupRelationship(user_id=user.uid, group_id=10)
            user.add_commit()
            user_group.add_commit()
            flash(gettext('Account created. You can now log in.'), 'success')
            signup_finished = True
    elif form.errors:
        if 'username' in form.errors:
            flash(gettext('Username must be between 4 and 32 characters'), 'danger')
        elif 'password' in form.errors:
            flash(gettext('Password must be between 6 and 64 characters'), 'danger')
        elif 'confirm_password' in form.errors:
            flash(gettext('Passwords must match'), 'danger')
        elif 'email' in form.errors:
            flash(gettext('Invalid email address'), 'danger')

    # If next param exists, redirect to that page
    if 'next' in request.args and signup_finished:
        return redirect(request.args.get('next'))
    elif signup_finished:
        return redirect(url_for('auth.login_page'))
    else:
        return render_template('auth/signup.html', form=form, user_exists=user_exists, title="Sign Up", page="signup")


@auth_blueprint.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash(gettext(u'You have been logged out.'), 'success')
    return redirect(url_for('main.index_page'))


@auth_blueprint.route('/user/<int:uid>')
@login_required
def user_page(uid):
    # Retrieve the user based on the userid
    user = User.query.get(uid)
    if not user:
        # Handle the case where the user doesn't exist
        return "User not found", 404
    # query the AccountGroupRelationship table for the user's account_id and the group's group_id
    group_relationship_json = user.get_groups()
    if group_relationship_json['msg'] == 'success':
        group_relationships = group_relationship_json['groups']
    else:
        group_relationships = []
    return render_template('auth/user.html', title="User Profile", page="user_profile",
                           user=user, groups=group_relationships)


# @auth_blueprint.route('/user/<int:uid>/edit')

@auth_blueprint.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('auth/dashboard.html', title="Dashboard", page="dashboard")
