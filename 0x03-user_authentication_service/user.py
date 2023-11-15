#!/usr/bin/env python3
"""
Module for creating user database
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    Creates database table users
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    session_id = Column(String(255))
    reset_token = Column(String(255))


if __name__ == "__main__":
    print(User.__tablename__)

    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))