#!/usr/bin/env python
# apis/repos.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
import requests
# 3rd party packages
from flask import jsonify, current_app

# local source
from .base import apis_blueprint, preprocess_request


@apis_blueprint.route('/repos', methods=['GET'])
def github_repo_data() -> jsonify:
    """
    Get GitHub repository data
    :argument: url, name, repo
    :return: GitHub repository data, 200 if success, 400 if missing parameter, 404 if not found
    """
    # Parse the arguments
    request_args = preprocess_request()
    repo_url = request_args.get('url')
    name = request_args.get('name')
    repo = request_args.get('repo')
    name_repo = f"{name}/{repo}" if name and repo else None

    if not repo_url and not name_repo:
        return jsonify({'status': 'error', 'message': 'Missing repository URL parameter'}), 400

    # Extract username and reponame from the GitHub URL
    if not name_repo:
        parts = repo_url.strip('/').split('/')
        if len(parts) < 3 or parts[-2] != 'github.com':
            return jsonify({'status': 'error', 'message': 'Invalid GitHub repository URL'}), 400

        username = parts[-3]
        reponame = parts[-1]
    else:
        if '/' not in name_repo or name_repo.count('/') > 1:
            return jsonify({'status': 'error', 'message': 'Invalid GitHub repository name'}), 400

        username, reponame = name_repo.split('/')

    # Construct the GitHub API URL
    api_url = f'https://api.github.com/repos/{username}/{reponame}'

    # Include your GitHub API token for authentication
    headers = {
        'Authorization': f'token {current_app.config["GITHUB_API_TOKEN"]}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        return jsonify({'status': 'success', 'message': 'GitHub repository data retrieved', 'data': repo_data})
    else:
        return jsonify({'status': 'error', 'message': 'GitHub repository not found'}), 404
