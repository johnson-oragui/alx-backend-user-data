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
        return False

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

    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.authorization_header())
    print(a.current_user())
