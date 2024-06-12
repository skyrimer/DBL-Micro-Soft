import os
from typing import Tuple


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
    env_var: str | None = os.getenv(env_var_str)
    assert (
        env_var is not None
    ), f"{env_var_str} is required but not found in environment variables"
    return env_var


def check_env_vars() -> Tuple[str, str, str, str]:
    """
    Check environment variables and return user, database, password, and host.

    Args:
        None

    Returns:
        tuple: A tuple containing user, database, password, and host strings.

    Raises:
        None
    """
    user: str = check_given_var("DBL_USER")
    database: str = check_given_var("DBL_DATABASE")
    password: str = check_given_var("DBL_PASSWORD")
    host: str = check_given_var("DBL_HOST")
    return user, database, password, host
