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


if __name__ == "__main__":
    """ Create a user test """
    user_email = str(uuid.uuid4())
    user_clear_pwd = str(uuid.uuid4())
    user = User()
    user.email = user_email
    user.first_name = "Bob"
    user.last_name = "Dylan"
    user.password = user_clear_pwd
    print("New user: {}".format(user.display_name()))
    user.save()

    """ Retreive this user via the class BasicAuth """

    a = BasicAuth()

    u = a.user_object_from_credentials(None, None)
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(89, 98)
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials("email@notfound.com", "pwd")
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(user_email, "pwd")
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(user_email, user_clear_pwd)
    print(u.display_name() if u is not None else "None")
