#!/usr/bin/env python
# apis/repos.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
import requests
# 3rd party packages
from flask import request, jsonify, current_app
# local source
from .base import apis_blueprint


@apis_blueprint.route('/repos', methods=['GET'])
def github_repo_data() -> (dict, int):
    repo_url = request.args.get('url')
    name = request.args.get('name')
    repo = request.args.get('repo')
    name_repo = name + '/' + repo if name and repo else None

    if not repo_url and not name_repo:
        return jsonify({'error': 'Missing repository URL parameter'}), 400

    # Extract username and reponame from the GitHub URL
    if not name_repo:
        parts = repo_url.strip('/').split('/')
        if len(parts) < 3 or parts[-2] != 'github.com':
            return jsonify({'error': 'Invalid GitHub repository URL'}), 400

        username = parts[-3]
        reponame = parts[-1]
    else:
        if '/' not in name_repo or name_repo.count('/') > 1:
            return jsonify({'error': 'Invalid GitHub repository name'}), 400

        username = name_repo[:name_repo.index('/')]
        reponame = name_repo[name_repo.index('/') + 1:]
    # Construct the GitHub API URL
    api_url = f'https://api.github.com/repos/{username}/{reponame}'

    # Include your GitHub API token for authentication
    # headers = {'Authorization': f'token {GITHUB_API_TOKEN}'}
    headers = {
        'Authorization': f'token {current_app.config["GITHUB_API_TOKEN"]}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        return jsonify(repo_data)
    else:
        return jsonify({'error': 'GitHub repository not found'}), 404
