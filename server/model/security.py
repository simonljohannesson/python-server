from server.integration.db_handler import DatabaseHandler
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


class Authenticator(object):
    @classmethod
    def user_password(cls, username, password):
        # get salt
        salt = DatabaseHandler.get_password_salt(username)
        # hash password
        hashed_password = hash_password(password, salt)
        # verify password
        password_valid = DatabaseHandler.authenticate(username, hashed_password)
        return password_valid


if __name__ == '__main__':
    valid = Authenticator().user_password("johnnyboi", "monkey123")
    print(valid)
