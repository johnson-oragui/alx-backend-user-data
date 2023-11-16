#!/usr/bin/env python3
"""
Module to hash password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Returns hashing of password in bytes
    """
    encoded_pwd = password.encode("utf-8")
    hashed_pwd = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())
    return hashed_pwd


if __name__ == "__main__":
    print(_hash_password("Hello Holberton"))
