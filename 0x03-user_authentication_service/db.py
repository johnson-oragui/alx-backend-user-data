#!/usr/bin/env python3
"""
DB module
"""
# Creates an SQLAlchemy database engine.
from sqlalchemy import create_engine
# The declarative base class from which all SQLAlchemy models inherit.
from sqlalchemy.exc import InvalidRequestError
# Session: Represents an active database session in SQLAlchemy.
# sessionmaker: A factory for creating new SQLAlchemy Session objects.
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
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

    def find_user_by(self, **kwargs) -> User:
        """
        Returns the first row found in the users table as filtered
        by the method’s input arguments.

        :param kwargs: Keyword arguments representing filter conditions.
        :return: User object if found, else raises NoResultFound.
        """
        # Check if all provided keys in kwargs are valid
        #   attributes of the User model
        if not all(hasattr(User, key) for key in kwargs.keys()):
            raise InvalidRequestError()

        # Query the database using filter_by to
        #   filter based on attribute values
        usr = self._session.query(User).filter_by(**kwargs).first()

        # If a user is found, return it; otherwise, raise NoResultFound
        if usr:
            return usr
        raise NoResultFound()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates the user attributes based on the provided keyword arguments.

        user_id: ID of the user to be updated.
        kwargs: User attributes and their new values.
        :raises ValueError: If an invalid attribute is provided.
        """
        try:
            # Find the user to update based on the provided user_id
            user_to_update = self.find_user_by(id=user_id)

            # Update user attributes based on keyword arguments
            for attr, value in kwargs.items():
                # Check if the attribute is a valid attribute of the User model
                if hasattr(User, attr):
                    setattr(user_to_update, attr, value)
                else:
                    # Raise a ValueError if an invalid attribute is provided
                    raise ValueError()
            # Commit the changes to the database
            self._session.commit()
        except NoResultFound:
            # Raise NoResultFound if no user is found with the specified ID
            raise NoResultFound()


if __name__ == "__main__":
    my_db = DB()
    email = 'test@test.com'
    hashed_password = "hashedPwd"

    user = my_db.add_user(email, hashed_password)
    print(user.id)

    try:
        my_db.update_user(user.id, hashed_password='NewPwd')
        print("Password updated")
    except ValueError:
        print("Error")
