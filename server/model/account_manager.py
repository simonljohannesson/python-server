from os import urandom
from server.utilities.hash import hash_password
from server.integration import db_handler

from server.integration.db_handler import DatabaseHandler

class AccountManager(object):
    """
    Class that handles user accounts.
    """
    def __init__(self, database_account_manager: db_handler.DatabaseHandler):
        self._account_manager = database_account_manager

    def add_user(self, username, password, email):
        """
        Add a user to the application.

        :param username:
        :param password:
        :param email:
        :return:
        """
        password_salt = str(urandom(32))
        password_hash = hash_password(password, password_salt)
        self._account_manager.add_user(username, email, password_hash, password_salt)


if __name__ == '__main__':
    dh = DatabaseHandler(None, debug=True)
    AccountManager(dh).add_user("monkeyman", "badman", "email")