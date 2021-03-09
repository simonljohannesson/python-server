from os import urandom

from server.model.token_manager import TokenCreationError, TokenExpiredError
from server.model.security import hash_password
from server.model import security
from server.model import token_manager
from server.integration.db_handler import DatabaseHandler


class AuthenticationError(Exception):
    def __init__(self, msg=None):
        if msg is None:
            super()
        else:
            super().__init__(msg)


def add_user(username, password, email):
    """
    Add a user to the application.

    :param username:
    :param password:
    :param email:
    :return:
    """
    password_salt = str(urandom(32))
    password_hash = hash_password(password, password_salt)
    DatabaseHandler.add_user(username, email, password_hash, password_salt)


def get_authentication_token(username, password) -> str:
    """
    Creates a new JWT token that can be used for authentication.

    :param username: users username
    :param password: users password
    :return: JWT token
    :raises TokenCreationError if creation of the token fails
    :raises AuthenticationError when there is a problem validating the username and password
    """
    auth = security.Authenticator()
    login_is_valid = auth.user_password(username, password)
    if login_is_valid:
        return token_manager.create_authentication_token(username)
    else:
        raise AuthenticationError("Failed to authenticate username and password.")

# TODO: validate token function that also checks against database


def get_user_from_authentication_token(token: str) -> bool:
    """
    Extracts the username from the JWT token.

    :param token
    :return: true if valid, false if not valid
    :raise token_manager.TokenInvalidError if token is not valid
    :raise token_manager.TokenExpiredError if token is expired
    """
    token_manager.validate_authentication_token(token)


if __name__ == '__main__':
    pass
