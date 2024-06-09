import os


def check_given_var(env_var_str: str) -> str:
    """
    Check if the given environment variable is set and return its value.

    Args:
        env_var_str (str): The name of the environment variable to check.

    Returns:
        str: The value of the environment variable.

    Raises:
        AssertionError: If the environment variable is not found.
    """

    env_var = os.getenv(env_var_str)
    assert (
        env_var is not None
    ), f"{env_var_str} is required but not found in environment variables"
    return env_var

def check_env_vars() -> (str, str, str, str):  # type: ignore
    user = check_given_var("DBL_USER")
    database = check_given_var("DBL_DATABASE")
    password = check_given_var("DBL_PASSWORD")
    host = check_given_var("DBL_HOST")
    return user, database, password, host