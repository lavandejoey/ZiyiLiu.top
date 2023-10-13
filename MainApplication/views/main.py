#!/usr/bin/env python
# views/main.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

import os

# standard library
# 3rd party packages
from flask import Blueprint, render_template, flash, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from flask_mail import Message
import logging

# local source
from MainApplication.forms import ContactForm

main_blueprint = Blueprint(name="main", import_name=__name__, static_folder="static",
                           template_folder="templates")


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


@main_blueprint.route('/files/<path:filename>')
@main_blueprint.route('/files/')
@login_required
def directory_page(filename=""):
    # Check if the user is logged in and belongs to the file manager group (1)
    if not current_user.is_authenticated:
        flash("You must be logged in to access this page.", "danger") if locale == "en" else flash("请先登录。", "danger")
        return redirect(request.referrer or url_for('main.index_page'))
    elif not current_user.belong_to_group(1):
        flash("You are not authorized to access this page.", "danger")
        return redirect(request.referrer or url_for('main.index_page'))
    root_path = os.path.join(current_app.root_path, "static", "files")
    # Ensure filename is a valid path within the root directory
    cur_dir = os.path.normpath(os.path.join(root_path, filename))
    # Check if the current directory is at the root
    at_root = cur_dir == root_path
    # Determine the parent directory
    par_dir = os.path.normpath(os.path.join(cur_dir, '..')) if not at_root else cur_dir
    # Get the current and parent directory names by removing the root path
    cur_dir_name = cur_dir.replace(root_path, "")[1:] if not at_root else cur_dir.replace(root_path, "")
    par_dir_name = par_dir.replace(root_path, "")[1:] if not at_root else par_dir.replace(root_path, "")
    # Initialize lists to store directory names, item counts, file names, and file sizes
    dir_list, dir_item_counts, file_list, file_sizes, file_sizes_unit = [], [], [], [], []
    # Iterate through the contents of the current directory
    for entry in os.listdir(cur_dir):
        entry_path = os.path.join(cur_dir, entry)
        if os.path.isdir(entry_path):
            dir_list.append(entry)
            dir_item_counts.append(len(os.listdir(entry_path)))
        elif os.path.isfile(entry_path):
            file_list.append(entry)
            # Get the file size in bytes, kilobytes, megabytes, gigabytes
            file_size = os.path.getsize(entry_path)
            for unit in ["B", "KB", "MB", "GB"]:
                if file_size < 1024:
                    file_sizes.append(file_size)
                    file_sizes_unit.append(unit)
                    break
                # Round to 4 decimal places
                file_size = round(file_size / 1024, 4)
    dir_dict = [{"name": dir_list[i], "items": dir_item_counts[i]} for i in range(len(dir_list))]
    file_dict = [{"name": file_list[i], "size": file_sizes[i], "unit": file_sizes_unit[i]} for i in
                 range(len(file_list))]
    # Sort by name
    dir_dict.sort(key=lambda x: x["name"])
    file_dict.sort(key=lambda x: x["name"])
    return render_template("main/files.html",
                           title="Files", page="files",
                           cur_dir_name=cur_dir_name, par_dir_name=par_dir_name, at_root=at_root,
                           dir_dict=dir_dict, file_dict=file_dict)
