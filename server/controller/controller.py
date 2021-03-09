from server.model import account_manager
from server.model.account_manager import AuthenticationError
from server.model.token_manager import TokenCreationError


class LoginException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            super()
        else:
            super().__init__(msg)


def login(username: str, password: str) -> str:
    """
    Logs in user and returns an authentication token.

    :param username:
    :param password:
    :return: authentication token
    """
    try:
        return account_manager.get_authentication_token(username, password)
    except (TokenCreationError, AuthenticationError):
        raise LoginException("Could not log in user.")
