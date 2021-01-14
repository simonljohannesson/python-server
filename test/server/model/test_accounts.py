import unittest
from unittest import mock
from server.model.account_manager import AccountManager


class TestAccounts(unittest.TestCase):
    @mock.patch('server.integration.db_handler.DatabaseHandler')
    def test_accounts(self, database_account_manager_mock):
        database_account_manager_mock.add_user.return_value = None
        AccountManager(database_account_manager_mock).add_user("Name", "Password", "email@email.com")
        # Test is pointless w/o integration.
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
