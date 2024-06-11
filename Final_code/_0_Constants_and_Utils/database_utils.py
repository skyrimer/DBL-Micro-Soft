import sqlite3
from typing import Any, Dict, List, Tuple, Union
import sys
import os
import mysql
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_0_Constants_and_Utils"))

from defined_paths import path_local_database, path_local_database_notebook
from env_vars import check_env_vars


def form_connection_params(local: bool, notebook: bool = False) -> Dict[str, str]:
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
    return dict(
            zip(["user", "database", "password", "host"], check_env_vars())
        )

def connect_to_database(connection_params: Dict[str, str], local: bool):
    """
    Connects to a database based on the provided connection parameters and local flag.

    Args:
        connection_params (Dict[str, str]): The parameters required to establish the database connection.
        local (bool): Flag indicating whether the connection should be local (SQLite) or remote (MySQL).

    Returns:
        Connection: The database connection object if successful.
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
        raise f"Error while connecting to MySQL: {e}" from e


def execute_queries(
    connection, queries: List[Union[str, Tuple[str, List[Tuple[Any]]]]]
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

    cursor = None
    cursor = connection.cursor()
    for query in queries:
        if isinstance(query, str):
            cursor.execute(query)
        else:
            sql, params = query
            cursor.executemany(sql, params)
    connection.commit()


def get_dataframe_from_query(query: str,
                             connection_params: Dict[str, str],
                             local: bool,
                             dtypes: Dict[str, str] = {},
                             index_col: str | None = None,
                             parse_dates: List[str] | None = None) -> pd.DataFrame:
    """
    Retrieves a pandas DataFrame by executing a query on a database connection.

    Args:
        query (str): The SQL query to execute.
        connection_params (Dict[str, str]): The parameters required to establish the database connection.
        local (bool): Flag indicating whether the connection is local (SQLite) or remote (MySQL).
        dtypes (Dict[str, str], optional): Dictionary specifying column data types.
            Defaults to {}.
        index_col (str | None, optional): Name of the column to set as the index.
            Defaults to None.
        parse_dates (List[str] | None, optional): List of columns to parse as dates.
            Defaults to None.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the results of the query.
    """

    if parse_dates:
        dtypes = {k: v for k, v in dtypes.items() if k not in parse_dates}

    if not local:
        url = f"mysql://{connection_params["user"]}:{connection_params["password"]}@{connection_params["host"]}:3306/{connection_params["database"]}"
        engine = create_engine(url)
        return pd.read_sql_query(query, engine, dtype=dtypes,
                                 index_col=index_col, parse_dates=parse_dates)
    
    with sqlite3.connect(connection_params["file_path"]) as connection:
        return pd.read_sql_query(
            query,
            connection,
            dtype=dtypes,
            index_col=index_col,
            parse_dates=parse_dates,
        )