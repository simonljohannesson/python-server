import unittest
from unittest import mock

from server.model.authenticator import Authenticator


class TestLoginManager(unittest.TestCase):

    def setUp(self) -> None:
        self.salt = "b'\\xf89\\x17\\x15B\\x8a\\xaa\\xcd\\x04I\\x8e\\x07\\xdd\\xce1x\\x91g\\x0e{\\xb0n\\x8e~\\t\\xf5\\xdc\\xa4\\x91T\\x8f\\xa2'"
        self.password = "monkey123"
        self.hashed_password = "b'\\x08\\x1b]\\x9e\\xe8\\n\\xa2^xw\\xa1\\xa2\\x82\\x7f\\xbf\\x86\\x18Ge\\xd5\\xa0\\x011\\xb2\\xed\\xd6\\xa3O\\xa5\\x1co2'"
        self.username = "johnnyboi"

    @mock.patch('server.integration.db_handler.DatabaseHandler')
    def test_authenticate(self, database_auth_mock):
        # set up mock
        database_auth_mock.get_password_salt.return_value = self.salt
        database_auth_mock.authenticate.return_value = True

        lm = Authenticator(database_auth_mock)
        actual_result = lm.authenticate(username=self.username, password=self.password)

        database_auth_mock.get_password_salt.assert_called_with(self.username)
        database_auth_mock.authenticate.assert_called_with(self.username, self.hashed_password)

        self.assertTrue(actual_result)


if __name__ == '__main__':
    unittest.main()
