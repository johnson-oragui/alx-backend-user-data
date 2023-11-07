#!/usr/bin/env python3
"""
Module for Basic Authentication
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Class that handles basic authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header for
        a Basic Authentication.
        """
        if authorization_header is None:
            return
        elif not isinstance(authorization_header, str):
            return
        elif not authorization_header.startswith("Basic "):
            return
        else:
            value = authorization_header.split(' ')
            return value[1]


if __name__ == "__main__":
    a = BasicAuth()

    print(a.extract_base64_authorization_header(None))
    print(a.extract_base64_authorization_header(89))
    print(a.extract_base64_authorization_header("Holberton School"))
    print(a.extract_base64_authorization_header("Basic Holberton"))
    print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
    print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))  # noqa
    print(a.extract_base64_authorization_header("Basic1234"))
