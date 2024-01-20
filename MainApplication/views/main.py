#!/usr/bin/env python
# views/main.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
import json
import os

# 3rd party packages
import requests
from flask import Blueprint, render_template, flash, request, current_app, redirect, url_for
from flask_babel import gettext
from flask_login import login_required, current_user
from flask_mail import Message

# local source
from MainApplication.extentions import cache
from MainApplication.forms import ContactForm

main_blueprint = Blueprint(name="main", import_name=__name__, static_folder="static",
                           template_folder="templates")


# The index page of the main application
@main_blueprint.route('/index')
@main_blueprint.route('/main')
@main_blueprint.route('/home')
@main_blueprint.route('/')
def index_page():
    return render_template("main/index.html", title=gettext("Joshua Ziyi Liu"), page="index")


@main_blueprint.route('/portfolio')
def portfolio_page():
    # cache get_github_data for different repo names
    @cache.memoize(timeout=60 * 60 * 24)  # 24 hours
    def get_github_data(_repo_name):
        usr = current_app.config["GITHUB_USERNAME"]
        with open("MainApplication/static/git-lang-colours.json", "r") as f:
            color_scheme = json.load(f)
        api_url = f'https://api.github.com/repos/{usr}/{_repo_name}'
        api_lang_url = f"https://api.github.com/repos/{usr}/{_repo_name}/languages"
        headers = {
            'Authorization': f'token {current_app.config["GITHUB_API_TOKEN"]}'
        }
        response_repo = requests.get(api_url, headers=headers)
        response_lang = requests.get(api_lang_url, headers=headers)
        if response_repo.status_code == 200 and response_lang.status_code == 200:
            repo = response_repo.json()
            languages = response_lang.json()
            total_lines = sum(languages.values())
            language_data = {
                key: {"percentage": round(val / total_lines * 100, 2), "color": color_scheme[key]["color"]}
                for key, val in languages.items()
            }
            repo["language"] = language_data
            return repo

    repos_json = []
    for repo_name in current_app.config["GITHUB_REPO_NAMES"]:
        repos_json.append(get_github_data(repo_name))
    return render_template("main/portfolio.html", title=gettext("Portfolio"), page="portfolio", repos=repos_json)


# Curriculum Vitae
@main_blueprint.route('/cv')
def cv_page():
    return render_template("main/cv.html", title=gettext("Curriculum Vitae"), page="cv")


# Contact me page
@main_blueprint.route('/contact', methods=['GET', 'POST'])
def contact_page():
    contact_form = ContactForm()
    csrf_token = request.form.get('csrf_token')
    if request.method == 'GET':
        return render_template("main/contact.html", title=gettext("Contact Me"), page="contact", form=contact_form,
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
        return render_template("main/contact.html", title=gettext("Contact Me"), page="contact", form=contact_form,
                               msg_sent=True)
    else:
        flash("Please check your input.")
        return render_template("main/contact.html", title=gettext("Contact Me"), page="contact", form=contact_form,
                               msg_sent=False)


@main_blueprint.route('/files/<path:filename>')
@main_blueprint.route('/files/')
@login_required
def directory_page(filename=""):
    # Check if the user is logged in and belongs to the file manager group (1)
    if not current_user.is_authenticated:
        # en, zh_Hans, zh_Hant, yue, fr
        flash(gettext("You must be logged in to access this page."), "danger")
        return redirect(request.referrer or url_for('main.index_page'))
    elif not current_user.belong_to_group("fileBrowser"):
        flash(gettext("You are not authorized to access this page."), "danger")
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
                           title=gettext("Files"), page="files",
                           cur_dir_name=cur_dir_name, par_dir_name=par_dir_name, at_root=at_root,
                           dir_dict=dir_dict, file_dict=file_dict)
