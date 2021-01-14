from server.integration import db_handler
from server.utilities.hash import hash_password


class LoginManager(object):
    def __init__(self, database_user_password_auth: db_handler.DatabaseUserAuthenticator):
        self._db_auth = database_user_password_auth

    def authenticate(self, username, password):
        # get salt
        salt = self._db_auth.get_password_salt(username)
        # hash password
        hashed_password = hash_password(password, salt)
        # verify password
        password_valid = self._db_auth.authenticate(username, hashed_password)
        return password_valid
