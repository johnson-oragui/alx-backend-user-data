#!/usr/bin/env python3
""" Module of Session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    Return
        - Logged in user
    """
    from api.v1.app import auth
    email = request.form.get('email')

    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        found_users = User.search(attributes={'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 401

    if not found_users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        found_user_bool = user.is_valid_password(password)
        if user.is_valid_password(password):
            found_user = user
    if not found_user_bool:
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(found_user.id)
    session_name = getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    Return:
        - Empty dictionary if succesful
    """
    from api.v1.app import auth

    deleted = auth.destroy_session(request)

    if not deleted:
        abort(404)

    return jsonify({}), 200
