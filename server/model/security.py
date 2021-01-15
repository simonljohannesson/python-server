from server.integration import db_handler
from server.utilities.hash import hash_password

from server.integration.db_handler import DatabaseHandler


class Authenticator(object):
    def __init__(self, database_user_password_auth: db_handler.DatabaseHandler):
        self._db_auth = database_user_password_auth

    def authenticate(self, username, password):
        # get salt
        salt = self._db_auth.get_password_salt(username)
        # hash password
        hashed_password = hash_password(password, salt)
        # verify password
        password_valid = self._db_auth.authenticate(username, hashed_password)
        return password_valid


if __name__ == '__main__':
    dh = DatabaseHandler(None, debug=True)
    valid = Authenticator(dh).authenticate("johnnyboi", "monkey123")
    print(valid)