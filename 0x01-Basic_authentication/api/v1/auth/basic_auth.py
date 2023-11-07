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


if __name__ == "__main__":
    a = BasicAuth()

    print(a.decode_base64_authorization_header(None))
    print(a.decode_base64_authorization_header(89))
    print(a.decode_base64_authorization_header("Holberton School"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
    print(a.decode_base64_authorization_header(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))  # noqa
