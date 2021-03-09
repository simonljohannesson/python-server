import os

# environment variables that are open to be fetched
_env_variables = {
    "AUTHENTICATION_TOKEN_SECRET",
    "DATABASE_NAME",
    "DATABASE_HOST_IP",
    "DATABASE_HOST_PORT",
    "PASSWORD_HASH_AUTHENTICATOR_PASSWORD",
    "APP_USER_MANAGER_PASSWORD"
}


def get(key: str) -> str:
    """
    Gets an environment variable.

    :param key:
    :param env_var:
    :return:
    """
    if key in _env_variables:
        env_var = os.getenv(key)
        if env_var is not None:
            return env_var
    raise RuntimeError("Environment variable", key, "is not defined or access is not permitted.")
