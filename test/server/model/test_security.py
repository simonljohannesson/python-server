import unittest
from unittest import mock

from server.model.security import Authenticator
from server.integration.db_handler import DatabaseHandler


salt = "b'\\xf89\\x17\\x15B\\x8a\\xaa\\xcd\\x04I\\x8e\\x07\\xdd\\xce1x\\x91g\\x0e{\\xb0n\\x8e~\\t\\xf5\\xdc\\xa4\\x91T\\x8f\\xa2'"
password = "monkey123"
hashed_password = "b'\\x08\\x1b]\\x9e\\xe8\\n\\xa2^xw\\xa1\\xa2\\x82\\x7f\\xbf\\x86\\x18Ge\\xd5\\xa0\\x011\\xb2\\xed\\xd6\\xa3O\\xa5\\x1co2'"
username = "johnnyboi"


class TestSecurity(unittest.TestCase):

    # def setUp(self) -> None:
        # salt = "b'\\xf89\\x17\\x15B\\x8a\\xaa\\xcd\\x04I\\x8e\\x07\\xdd\\xce1x\\x91g\\x0e{\\xb0n\\x8e~\\t\\xf5\\xdc\\xa4\\x91T\\x8f\\xa2'"
        # password = "monkey123"
        # hashed_password = "b'\\x08\\x1b]\\x9e\\xe8\\n\\xa2^xw\\xa1\\xa2\\x82\\x7f\\xbf\\x86\\x18Ge\\xd5\\xa0\\x011\\xb2\\xed\\xd6\\xa3O\\xa5\\x1co2'"
        # username = "johnnyboi"

    @mock.patch('server.model.integration_bridge.IntegrationBridge.get_password_salt', return_value=salt)
    @mock.patch('server.model.integration_bridge.IntegrationBridge.authenticate', return_value=True)
    def test_authenticate(self, mk2, mk1):
        auth = Authenticator()
        actual_result = auth.user_password(username=username, password=password)

        mk1.assert_called_with(username)
        mk2.assert_called_with(username, hashed_password)

        self.assertTrue(actual_result)

    @mock.patch('server.model.integration_bridge.IntegrationBridge')
    def test_authenticate_2(self, mk1):
        print(DatabaseHandler() is mk1())

        # auth = Authenticator()
        # actual_result = auth.user_password(username=username, password=password)
        # # get_password_salt', return_value=salt
        #
        # self.assertTrue(actual_result)


if __name__ == '__main__':
    unittest.main()
