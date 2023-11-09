#!/usr/bin/env python3
"""
Module for SessionAuth Class
"""
import uuid
from typing import Optional
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth authentication Class
    """
    # attr to store user_id as session using uuid as key
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> Optional[str]:
        """
        Method to create a sessiion Id for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return
        # generate uuid for the session key
        session_id = str(uuid.uuid4())
        # set the user_id as value to session key
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user_id based on the session_id
        """
        if session_id is None or not isinstance(session_id, str):
            return
        # Use .get() to access the User ID based on the Session ID
        return SessionAuth.user_id_by_session_id.get(session_id)
