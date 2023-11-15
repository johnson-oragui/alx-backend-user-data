#!/usr/bin/env python3
"""
DB module
"""
# Creates an SQLAlchemy database engine.
from sqlalchemy import create_engine
# The declarative base class from which all SQLAlchemy models inherit.
from sqlalchemy.ext.declarative import declarative_base
# Session: Represents an active database session in SQLAlchemy.
# sessionmaker: A factory for creating new SQLAlchemy Session objects.
from sqlalchemy.orm import sessionmaker, Session
from user import Base, User


# DB class encapsulates database-related functionality.
class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        # Creates an SQLite database engine pointing to "a.db"
        #   with echoing SQL statements
        self._engine = create_engine("sqlite:///a.db")
        # Drops existing tables
        Base.metadata.drop_all(self._engine)
        # creates new ones based on the models defined in user.py.
        Base.metadata.create_all(self._engine)
        # Initializes the private __session attribute to None.
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoize session object
        """
        # Checks if the private __session attribute is None.
        if self.__session is None:
            # If it is, creates a new DBSession using the database
            #   engine and assigns it to __session.
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
            # Returns the current value of __session.
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Saves the user to the database
        """
        # create an instance of User, adding values to the table
        usr = User(email=email, hashed_password=hashed_password)
        # adding to session
        self._session.add(usr)
        # saving to session
        self._session.commit()
        return usr


if __name__ == "__main__":
    my_db = DB()

    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(user_1.id)

    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(user_2.id)
