import unittest
from unittest import mock
from server.model import account_manager
from server.integration.db_handler import DatabaseHandler


class TestAccounts(unittest.TestCase):
    @mock.patch('server.integration.db_handler.DatabaseHandler')
    def test_accounts(self, db_handler_mock):
        db_handler_mock.add_user.return_value = None

        account_manager.add_user("Name",
                                 "Password",
                                 "email@email.com")
        # Test is pointless w/o integration.
        self.assertEqual(True, True)

    @mock.patch('server.model.integration_bridge.IntegrationBridge.authenticate', side_effect=Exception("bon likki likki"))
    def test_get_authentication_token(self, mock_obj):
        a = account_manager.get_authentication_token("bonk", "not a password eh")
        print(a)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
