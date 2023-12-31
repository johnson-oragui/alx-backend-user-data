#!/usr/bin/env python3
"""
Module to manage the API authentication.
"""
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


if __name__ == "__main__":
    a = Auth()

    print(a.require_auth(None, None))
    print(a.require_auth(None, []))
    print(a.require_auth("/api/v1/status/", []))
    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/",
                         "/api/v1/stats"]))
