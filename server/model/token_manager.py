import jwt
import datetime
from server.config import config

_ENCODING_ALGORITHM = "HS512"


class TokenCreationError(Exception):
    pass


def create_authentication_token(user_name: str) -> str:
    """
    Generates a new authentication token.

    :param user_name:
    :raises token_manager.TokenCreationError
    :return:
    """
    # payload
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8.0),
        "iat": datetime.datetime.utcnow(),
        "sub": user_name
    }
    try:
        # sign
        token = jwt.encode(
            payload,
            config.get("AUTHENTICATION_TOKEN_SECRET"),
            _ENCODING_ALGORITHM)
        return token
    except jwt.exceptions.InvalidTokenError as error:
        # TODO: jwt base exception, possible issue, should log
        raise TokenCreationError()


class TokenInvalidError(Exception):
    def __init__(self, msg=None):
        if msg is None:
            super()
        else:
            super().__init__(msg)


class TokenExpiredError(Exception):
    def __init__(self, msg=None):
        if msg is None:
            super()
        else:
            super().__init__(msg)


def validate_authentication_token(jwt_token: str) -> str:
    """
    Validates a jwt authentication token and returns the user_name
    associated with the token if the token is valid.

    :param jwt_token: token to validate
    :return: user_name valid user name
    :raise token_manager.TokenInvalidError if token is not valid
    :raise token_manager.TokenExpiredError if token is expired
    """
    try:
        jwt_claims = jwt.decode(jwt_token,
                                config.get("AUTHENTICATION_TOKEN_SECRET"),
                                _ENCODING_ALGORITHM,
                                options={
                                    "verify_signature": True,
                                })
        user_name = jwt_claims["sub"]
        return user_name
    except jwt.exceptions.ExpiredSignatureError as error:
        raise TokenExpiredError()
    except jwt.exceptions.InvalidSignatureError as error:
        # TODO: possible malicious activity, signature does not match, should log
        raise TokenInvalidError("Token could not be validated.")
    except jwt.exceptions.InvalidTokenError as error:
        # TODO: jwt base exception, possible issue, should log
        raise TokenInvalidError("Token could not be validated.")
    except KeyError as error:
        # TODO: possible issue, should log
        raise TokenInvalidError("Token could not be validated due to missing sub in payload.")

