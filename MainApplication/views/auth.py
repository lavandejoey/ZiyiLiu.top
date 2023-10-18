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
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_

from MainApplication.apis import get_locale
# local source
from MainApplication.forms import LoginForm, SignupForm
from MainApplication.models import User, AccountGroupRelationship

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
                flash('Login successful', 'success') if get_locale() == 'en' else None
                flash('登录成功', 'success') if get_locale() == 'zh_Hans' else None
                flash('登錄成功', 'success') if get_locale() == 'zh_Hant' or get_locale() == 'yue' else None
                flash('Connexion réussie', 'success') if get_locale() == 'fr' else None
                return redirect(url_for('auth.user_page', uid=user.uid))
            else:
                password_error = True
                flash('Incorrect password', 'danger') if get_locale() == 'en' else None
                flash('密码错误', 'danger') if get_locale() == 'zh_Hans' else None
                flash('密碼錯誤', 'danger') if get_locale() == 'zh_Hant' or get_locale() == 'yue' else None
                flash('Mot de passe incorrect', 'danger') if get_locale() == 'fr' else None
        else:
            user_not_found = True
            flash('User not found', 'danger') if get_locale() == 'en' else None
            flash('用户不存在', 'danger') if get_locale() == 'zh_Hans' else None
            flash('用戶不存在', 'danger') if get_locale() == 'zh_Hant' or get_locale() == 'yue' else None
            flash('Utilisateur non trouvé', 'danger') if get_locale() == 'fr' else None

    return render_template('auth/login.html', title="Login", page="login",
                           form=form, user_not_found=user_not_found, password_error=password_error)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('auth.user_page', uid=current_user.uid))

    form = SignupForm()
    user_exists = False
    if form.validate_on_submit():
        username, password, email, phone = form.username.data, form.password.data, form.email.data, form.phone.data
        # Check if any of the parameters already exist in the database
        existing_user = User.query.filter(
            or_(User.username == username, User.email == email)).first()

        if existing_user:
            user_exists = True
        else:
            # Create a new user and save it to the database
            user = User(username=username, email=email, phone=phone)
            user.set_password(password)
            user.add_commit()
            # Link the user to the group (user as default)
            user_group = AccountGroupRelationship(account_id=user.uid, group_id=1)
            user_group.add_commit()

            flash('Account created. You can now log in.', 'success') if get_locale() == 'en' else None
            flash('账户已创建。您现在可以登录。', 'success') if get_locale() == 'zh_Hans' else None
            flash('賬戶已創建。您現在可以登錄。',
                  'success') if get_locale() == 'zh_Hant' or get_locale() == 'yue' else None
            flash('Compte créé. Vous pouvez maintenant vous connecter.', 'success') if get_locale() == 'fr' else None
    elif form.errors.get('confirm_password'):
        flash('Passwords must match', 'danger') if get_locale() == 'en' else None
        flash('密码必须匹配', 'danger') if get_locale() == 'zh_Hans' else None
        flash('密碼必須匹配', 'danger') if get_locale() == 'zh_Hant' or get_locale() == 'yue' else None
        flash('Les mots de passe doivent correspondre', 'danger') if get_locale() == 'fr' else None

    return render_template('auth/signup.html', form=form, user_exists=user_exists,
                           title="Sign Up", page="signup")


@auth_blueprint.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You have been logged out.', 'success') if get_locale() == 'en' else None
    flash('您已注销。', 'success') if get_locale() == 'zh_Hans' else None
    flash('您已註銷。', 'success') if get_locale() == 'zh_Hant' or get_locale() == 'yue' else None
    flash('Vous avez été déconnecté.', 'success') if get_locale() == 'fr' else None
    return redirect(url_for('main.index_page'))


@auth_blueprint.route('/user/<int:uid>')
@login_required
def user_page(uid):
    # Retrieve the user based on the userid
    user = User.query.get(uid)
    if not user:
        # Handle the case where the user doesn't exist
        return "User not found", 404

    # You can now render the user's profile page
    return render_template('auth/user.html', user=user, title="User Profile", page="user_profile")
