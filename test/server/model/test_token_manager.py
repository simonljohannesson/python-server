import datetime
import unittest
import server.model.token_manager as TokenManager
import jwt
from server.config import config


class TestTokenManager(unittest.TestCase):
    def test_create_validate(self):
        expected_name = "some_name"

        manufactured_payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            "iat": datetime.datetime.utcnow(),
            "sub": expected_name
        }
        encoded_token = jwt.encode(
            manufactured_payload,
            config.get("AUTHENTICATION_TOKEN_SECRET"),
            TokenManager._ENCODING_ALGORITHM
        )

        actual_name = TokenManager.validate_authentication_token(encoded_token)
        self.assertEqual(expected_name, actual_name)

    def test_validate_expired_token(self):
        manufactured_payload = {
            "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=10), # expired
            "iat": datetime.datetime.utcnow(),
            "sub": "user_name"
        }
        encoded_token = jwt.encode(
            manufactured_payload,
            config.get("AUTHENTICATION_TOKEN_SECRET"),
            TokenManager._ENCODING_ALGORITHM
        )
        self.assertRaises(
            TokenManager.TokenExpiredError,
            TokenManager.validate_authentication_token,
            encoded_token
        )

    def test_validate_bad_signature_token(self):
        manufactured_payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=10),
            "iat": datetime.datetime.utcnow(),
            "sub": "user_name"
        }
        encoded_token = jwt.encode(
            manufactured_payload,
            "not the real secret", # bad secret used
            TokenManager._ENCODING_ALGORITHM
        )
        self.assertRaises(
            TokenManager.TokenInvalidError,
            TokenManager.validate_authentication_token,
            encoded_token
        )

    def test_validate_missing_sub_token(self):
        manufactured_payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=10),
            "iat": datetime.datetime.utcnow() + datetime.timedelta(hours=10),
        }
        encoded_token = jwt.encode(
            manufactured_payload,
            config.get("AUTHENTICATION_TOKEN_SECRET"),
            TokenManager._ENCODING_ALGORITHM
        )
        self.assertRaises(
            TokenManager.TokenInvalidError,
            TokenManager.validate_authentication_token,
            encoded_token
        )


if __name__ == '__main__':
    unittest.main()
