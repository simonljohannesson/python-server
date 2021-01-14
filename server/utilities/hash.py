"""
Module that will handle hashing.
"""
import hashlib


def hash_password(password: str, salt: str) -> str:
    """
    Hash a password using a salt.

    :param password: password that should be hashed
    :param salt: salt to use when hashing password
    :return: hashed password
    """
    return str(hashlib.pbkdf2_hmac(
        "sha256",
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000))
