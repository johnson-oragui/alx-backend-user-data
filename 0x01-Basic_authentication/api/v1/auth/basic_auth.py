#!/usr/bin/env python3
"""
Module for Basic Authentication
"""
import base64
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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:  # noqa
        """
        Returns the decoded value of a Base64 string
            base64_authorization_header
        """
        if base64_authorization_header is None:
            return
        if not isinstance(base64_authorization_header, str):
            return
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
        except Exception:
            return
        else:
            return decoded_str

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # noqa
        """
        Returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        user, pwd = decoded_base64_authorization_header.split(':')
        return user, pwd


if __name__ == "__main__":
    a = BasicAuth()

    print(a.extract_user_credentials(None))
    print(a.extract_user_credentials(89))
    print(a.extract_user_credentials("Holberton School"))
    print(a.extract_user_credentials("Holberton:School"))
    print(a.extract_user_credentials("bob@gmail.com:toto1234"))
