import os
import sqlite3
import sys
from itertools import islice
from typing import Any, Dict, List, Optional, Tuple, Union

import mysql.connector
import pandas as pd
from mysql.connector import Error
from sqlalchemy import create_engine

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "_0_Constants_and_Utils",
    )
)

from defined_paths import path_local_database, path_local_database_notebook
from env_vars import check_env_vars


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
    env_var: Optional[str] = os.getenv(env_var_str)
    assert (
        env_var is not None
    ), f"{env_var_str} is required but not found in environment variables"
    return env_var


def form_connection_params(local: bool, notebook: bool = False) -> Dict[str, Any]:
    """
    Forms connection parameters based on the local and notebook flags.

    Args:
        local (bool): Flag indicating whether the connection is local.
        notebook (bool, optional): Flag indicating whether the notebook
            environment is used. Defaults to False.

    Returns:
        Dict[str, str]: A dictionary containing connection parameters based on the flags.
    """
    if local:
        if notebook:
            return {"file_path": path_local_database_notebook}
        else:
            return {"file_path": path_local_database}
    return dict(zip(["user", "database", "password", "host"], check_env_vars()))


def connect_to_database(
    connection_params: Dict[str, str], local: bool
) -> Union[sqlite3.Connection, mysql.connector.MySQLConnection]:
    """
    Connects to a database based on the provided connection parameters and local flag.

    Args:
        connection_params (Dict[str, str]): The parameters required to establish the database connection.
        local (bool): Flag indicating whether the connection should be local (SQLite) or remote (MySQL).

    Returns:
        Union[sqlite3.Connection, mysql.connector.MySQLConnection]: The database connection object if successful.

    Raises:
        Error: If an error occurs during the connection process.
    """
    if local:
        return sqlite3.connect(connection_params["file_path"])
    try:
        connection = mysql.connector.connect(
            user=connection_params["user"],
            database=connection_params["database"],
            password=connection_params["password"],
            host=connection_params["host"],
            connect_timeout=10,
        )
        if connection.is_connected():
            return connection
    except Error as e:
        raise ConnectionError(f"Error while connecting to MySQL: {e}") from e


def execute_queries(
    connection: Union[sqlite3.Connection, mysql.connector.MySQLConnection],
    queries: List[Union[str, Tuple[str, List[Tuple[Any]]]]],
) -> None:
    """
    Executes a list of SQL queries on the provided database connection.

    Args:
        connection: The database connection object.
        queries (List[Union[str, Tuple[str, List[Tuple[Any]]]]): A list of SQL
            queries to execute, where each query can be a string or a tuple
            containing the SQL query and parameters.

    Returns:
        None
    """
    cursor = connection.cursor()
    for query in queries:
        if isinstance(query, str):
            cursor.execute(query)
        else:
            sql, params = query
            cursor.executemany(sql, params)
    connection.commit()


def get_dataframe_from_query(
    query: str,
    connection_params: Dict[str, str],
    local: bool,
    dtypes: Optional[Dict[str, str]] = None,
    index_col: Optional[str] = None,
    parse_dates: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Retrieves a pandas DataFrame by executing a query on a database connection.

    Args:
        query (str): The SQL query to execute.
        connection_params (Dict[str, str]): The parameters required to establish the database connection.
        local (bool): Flag indicating whether the connection is local (SQLite) or remote (MySQL).
        dtypes (Optional[Dict[str, str]], optional): Dictionary specifying column data types.
            Defaults to None.
        index_col (Optional[str], optional): Name of the column to set as the index.
            Defaults to None.
        parse_dates (Optional[List[str]], optional): List of columns to parse as dates.
            Defaults to None.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the results of the query.
    """
    if parse_dates:
        dtypes = {k: v for k, v in (dtypes or {}).items() if k not in parse_dates}

    if not local:
        url: str = (
            f"mysql+mysqlconnector://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:3306/{connection_params['database']}"
        )
        engine = create_engine(url)
        return pd.read_sql_query(
            query, engine, dtype=dtypes, index_col=index_col, parse_dates=parse_dates
        )

    with sqlite3.connect(connection_params["file_path"]) as connection:
        return pd.read_sql_query(
            query,
            connection,
            dtype=dtypes,
            index_col=index_col,
            parse_dates=parse_dates,
        )


def split_into_batches(lst: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Splits a list into batches of a specified size using itertools.

    Args:
        lst (List[Any]): The input list to be split into batches.
        batch_size (int): The size of each batch.

    Returns:
        List[List[Any]]: A list of batches of the input list based on the specified batch size.
    """
    it = iter(lst)
    return iter(lambda: list(islice(it, batch_size)), [])
