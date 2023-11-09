#!/usr/bin/env python3
"""
Route module for the API
"""
import os
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from typing import Optional

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
# create auth to store authentication instance, starting it with None
auth = None
# assign the right instance of authentication to auth
auth_type = getenv("AUTH_TYPE")
# checks to assign the right instance to auth
if auth_type == "auth":
    # import Auth for assigning of right instance
    from api.v1.auth.auth import Auth
    auth = Auth()
if auth_type == "basic_auth":
    # import BasicAuth for assigning of right instance
    from api.v1.auth.basic_auth impiort BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handles unauthorised error
    """
    response = jsonify({"error": "Unauthorized"})

    return response, 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handles forbidden error
    """
    response = jsonify({"error": "Forbidden"})

    return response, 403


# handles request filtering
@app.before_request
def before_request() -> Optional[str]:
    """
    Filtering of each request before action
    The @app.before_request decorator registers this function to be executed
    before each request.
    """
    # create a list of allowed paths
    allowed_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                     '/api/v1/forbidden/']
    # check for if auth is None,i.e no instance is assigned to auth
    if auth is None:
        # do nothing
        return
    # checks if request.path is not part of allowed_paths
    if not auth.require_auth(request.path, allowed_paths):
        # do nothing if it is not part of the list
        return
    # checks if the auth method 'authorization_header' returned None
    if auth.authorization_header(request) is None:
        # if it does, raise error with status code 401
        abort(401)  # unauthorized access.
    # checks if the auth method 'current_user' returned None
    if auth.current_user(request) is None:
        # if it does, raise error with status code 403
        raise abort(403)  # forbidden access.


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
