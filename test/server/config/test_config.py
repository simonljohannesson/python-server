import unittest
from server.config import config


class TestConfig(unittest.TestCase):
    def test_config_not_none(self):
        result = config.get("AUTHENTICATION_TOKEN_SECRET")
        self.assertTrue(result is not None)

    def test_config_not_available(self):
        result = config.get("AUTHENTICATION_TOKEN_SECRET")
        self.assertRaises(
            RuntimeError,
            config.get,
            "this is never going to be an available config setting"
        )


if __name__ == '__main__':
    unittest.main()
