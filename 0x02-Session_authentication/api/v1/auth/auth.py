#!/usr/bin/env python3
"""
Module to manage the API authentication.
"""
import os
from os import getenv
from flask import request
from typing import List, TypeVar, Optional


class Auth():
    """
    manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required to access path.
        """
        if not excluded_paths or excluded_paths == [] or not path:
            return True
        # excluded_paths always ends with '/'
        path = path if path.endswith('/') else path + '/'
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.strip('*')):
                return False
        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """
        Checks for authorization header in request
        """
        # create a variable key and assign authorization
        key = "Authorization"
        # check for request been none and key absent in request header
        if request is None or key not in request.headers:
            # return none in regards to the check
            return None
        # return authorization as a single header in the response obj
        return request.headers.get(key)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Only Returns None
        """
        return

    def session_cookie(self, request=None) -> Optional[str]:
        """
        Return the value of the cookie from request
        """
        if request is None:
            print("request is None")
            return
        # retrieve the session_name from the env variable
        session_name = getenv("SESSION_NAME", "_my_session_id")
        #print(f"session_name: {session_name}")
        #print(f"request.cookies.get: {request.cookies.get(session_name)}")
        if request.cookies.get(session_name):
            return request.cookies.get(session_name)
        # return the value of cokkie
        return f"_my_session_id"


if __name__ == "__main__":
    pass
