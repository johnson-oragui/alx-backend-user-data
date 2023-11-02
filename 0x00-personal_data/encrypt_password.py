#!/usr/bin/env python3
""" Password encryption module """
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """
    encoded_pwd = password.encode()
    hashed_pwd = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if hashed password matches unhashed password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    encrypted_password = hash_password(password)
    print(encrypted_password)
    print(is_valid(encrypted_password, password))
