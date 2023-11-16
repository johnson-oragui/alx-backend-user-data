#!/usr/bin/env python3
"""
Module to hash password and interact with auth DB
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
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

    def create_session(self, email: str) -> Optional[str]:
        """
        Create a session for the user identified by the provided email.

        param email: Email address of the user.
        return: Session ID if created successfully, otherwise None.
        """
        try:
            # Attempt to find the user by the provided email
            existing_user = self._db.find_user_by(email=email)

            # Generate a new session ID using a helper function
            session_id = _generate_uuid()

            # Update the user's session ID in the database
            self._db.update_user(existing_user.id, session_id=session_id)

            # Return the generated session ID
            return session_id
        except NoResultFound:
            # If no user is found with the provided email, return None
            return

    def get_user_from_session_id(self, session_id: str) -> Optional[str]:
        """
        Get the user associated with the provided session ID.

        session_id: Session ID to identify the user.
        return: User object if found, otherwise None.
        """
        try:
            # Attempt to find the user by the provided session_id
            existing_user = self._db.find_user_by(session_id=session_id)
            # If a user with the provided session_id is found
            if existing_user:
                # Return the user object
                return existing_user
            # If no user is found with the provided session_id, return None
            return
        except Exception:
            # Handle any exceptions that might occur during the process
            return

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the session associated with the given user ID.

        user_id: ID of the user whose session needs to be destroyed.
        return: None
        """
        try:
            # Attempt to find the user by the provided user ID
            user = self._db.find_user_by(id=user_id)
            # Set the session ID to None, effectively destroying the session
            user.session_id = None
        except Exception:
            return

    def get_reset_password_token(self, email: str) -> Optional[str]:
        """
        Generates and retrieves a reset password token for the user.

        This method generates a unique reset password token, associates it
        with the user identified by the provided email, and returns the token.

        email (str): Email address of the user for whom the token is generated.

        Returns:
        - str: The generated reset password token.

        Raises:
        - ValueError: If the provided email does not correspond to an existing
                    user or if an unexpected error occurs during the process.
        """
        try:
            # Attempt to find the user by the provided email
            existing_user = self._db.find_user_by(email=email)

            # If a user with the provided email is found
            if existing_user:
                # Generate a new reset password token using a UUID
                token = str(uuid.uuid4())

                # Associate the token with the user in the database
                existing_user.reset_token = token

                # Return the generated reset password token
                return token
            else:
                # If no user is found with the provided email, raise ValueError
                raise ValueError

        except Exception:
            # Handle unexpected exceptions and raise ValueError
            raise ValueError


if __name__ == "__main__":
    pass
