#!/usr/bin/env python3
"""
Route module for the API
"""
import os
from os import getenv
from typing import Optional
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.views import app_views

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
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif auth_type == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(_) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(_) -> str:
    """
    Handles unauthorised error
    """
    response = jsonify({"error": "Unauthorized"})

    return response, 401


@app.errorhandler(403)
def forbidden(_) -> str:
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
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']
    # check for if auth is None,i.e no instance is assigned to auth
    if auth is None:
        return
    if not auth.require_auth(request.path, allowed_paths):
        return
    if not auth.authorization_header(request) and not auth.session_cookie(request):  # noqa
        return abort(401)
    if not auth.current_user(request):
        return abort(403)
    if auth.current_user(request):
        request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
