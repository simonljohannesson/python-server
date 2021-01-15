import os

# environment variables that are open to be fetched
_env_variables = {
    "AUTHENTICATION_TOKEN_SECRET"
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
        return str(env_var)
        # if env_var is not None:
        #     return env_var
    raise RuntimeError("Environment variable", key, "is not defined or access is not permitted.")
