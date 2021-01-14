from server.integration import db_handler
from server.utilities.hash import hash_password


class LoginManager(object):
    def __init__(self, database_user_password_auth: db_handler.DatabaseUserAuthenticator):
        self._db_auth = database_user_password_auth

    def authenticate(self, username, password):
        # get salt
        salt = self._db_auth.get_password_salt(username)
        # hash password
        # hashed_password = password
        hashed_password = hash_password(password, salt)
        print(hashed_password)
        copy = "b'\\x08\\x1b]\\x9e\\xe8\\n\\xa2^xw\\xa1\\xa2\\x82\\x7f\\xbf\\x86\\x18Ge\\xd5\\xa0\\x011\\xb2\\xed\\xd6\\xa3O\\xa5\\x1co2'"
        print(copy)
        print(hashed_password == copy)
        # verify password
        password_valid = self._db_auth.authenticate(username, hashed_password)
        return password_valid
