#!/usr/bin/env python3
"""
Module to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Only Returns False
        """
        if not excluded_paths or excluded_paths == [] or not path:
            return True
        # excluded_paths always ends with '/'
        path = path if path.endswith('/') else path + '/'
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.strip('*')):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Just Returns None
        """
        return

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
