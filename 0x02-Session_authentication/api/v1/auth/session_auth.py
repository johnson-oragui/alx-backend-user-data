#!/usr/bin/env python3
"""
Module for SessionAuth
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth authentication
    """
    # attr to store user_id as session using uuid as key
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Method to create a sessiion Id for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return
        # generate uuid for the session key
        session_id = str(uuid.uuid4())
        # set the user_id as value to session key
        SessionAuth.user_id_by_session_id.get(session_id) = user_id
        return session_id
