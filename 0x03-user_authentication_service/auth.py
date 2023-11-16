#!/usr/bin/env python3
"""
Module to hash password and interact with auth DB
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    password: Raw unhashed password.
    return: Hashed password as bytes.
    """
    # Encode the password as bytes using UTF-8
    encoded_pwd = password.encode("utf-8")

    # Hash the encoded password using bcrypt with a generated salt
    hashed_pwd = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())

    # Return the hashed password as bytes
    return hashed_pwd


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self) -> None:
        """
        Initialize Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user and returns a User object.

        email: User's email.
        password: User's password.
        return: User object.
        raises ValueError: If the user with the given email already exists.
        """
        try:
            # Check if a user with the same email already exists
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user is found, continue with registration
            pass
        # Hash the password
        hashed_pwd = _hash_password(password)
        # Add the user to the database
        new_usr = self._db.add_user(email=email,
                                    hashed_password=hashed_pwd.decode("utf-8"))
        # Save the user to the database
        self._db
        # Return new user
        return new_usr


if __name__ == "__main__":
    email = 'me@me.com'
    password = 'mySecuredPwd'

    auth = Auth()

    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print("could not create a new user: {}".format(err))

    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print("could not create a new user: {}".format(err))
