#!/usr/bin/env python
# routes.py

# standard library

# 3rd party packages
from flask import render_template, request, redirect, jsonify

# local source
from mainApp import db
from mainApp.models import User


def create_routes(app):
    @app.route('/')
    def index():
        return render_template('homepage.html')

    @app.route('/about')
    def about():
        return render_template('blog_layout.html')

    @app.route('/add', methods=['POST'])
    def add_user():
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect('/')

    @app.route('/users', methods=['GET', 'POST'])
    def users():
        if request.method == 'POST':
            # Create a new user
            username = request.json['username']
            email = request.json['email']
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201

        # Get all users
        users = User.query.all()
        results = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            for user in users
        ]
        return jsonify(results)
