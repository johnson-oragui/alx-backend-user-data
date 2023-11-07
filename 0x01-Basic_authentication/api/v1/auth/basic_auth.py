#!/usr/bin/env python3
"""
Module for Basic Authentication
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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
        user, pwd = decoded_base64_authorization_header.split(':', maxsplit=1)
        return user, pwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # noqa
        """
        Returns the User instance based on his email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return
        if user_pwd is None or not isinstance(user_pwd, str):
            return
        try:
            users = User.search(attributes={"email": user_email})
        except KeyError:
            return None

        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validates credentials passed in 'Authorization' header'
            Returns:
                - User object associated with valid credentials
        """
        auth_header = self.authorization_header(request)

        b64_str = self.extract_base64_authorization_header(auth_header)

        decode_b64_str = self.decode_base64_authorization_header(b64_str)

        email, pwd = self.extract_user_credentials(decode_b64_str)

        user = self.user_object_from_credentials(email, pwd)

        return user
