#!/usr/bin/env python3
"""
Module to hash password and interact with auth DB
"""
import bcrypt
import uuid
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


def _generate_uuid() -> str:
    """
    Return a string representation of a new UUID.
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login credentials.

        email: Email address of the user.
        password: Password provided by the user.
        return: True if login credentials are valid, False otherwise.
        """
        try:
            # Attempt to find the user by the provided email
            existing_user = self._db.find_user_by(email=email)
            # If a user with the provided email is found
            if existing_user:
                # encode the provided login password
                encoded_hashed_pwd = password.encode()
                # retrieve the hashed_password from the database and encode it
                user_pwd_bytes = existing_user.hashed_password.encode('utf-8')
                # Compare the encoded login password with
                #   the stored hashed password
                return bcrypt.checkpw(encoded_hashed_pwd, user_pwd_bytes)
            else:
                return False
        # Handle the case where no user is found with the provided email
        except NoResultFound:
            return False


if __name__ == "__main__":
    email = 'bob@bob.com'
    password = 'MyPwdOfBob'
    auth = Auth()

    auth.register_user(email, password)

    print(auth.valid_login(email, password))

    print(auth.valid_login(email, "WrongPwd"))

    print(auth.valid_login("unknown@email", password))
