import pandas as pd
import sqlite3
from sqlalchemy import create_engine

from Final_code._0_Constants.env_vars import check_env_vars
from Final_code._0_Constants.viz_constants import DTYPES

# This is a file with functions used to get data from the sql server and put it in a DataFrame

def get_local_data(query: str, path: str, dtype: bool = True) -> pd.DataFrame:
    # Connect to the SQLite database using a context manager
    with sqlite3.connect(path) as connection:
        # Read the data into a DataFrame
        if dtype:
            df = pd.read_sql_query(query, connection,
                                   dtype={k: v for k, v in DTYPES.items() if
                                          k not in ("tweet_creation_time", "user_creation_time")},
                                   index_col='tweet_id')
            df['tweet_creation_time'] = pd.to_datetime(df['tweet_creation_time'])
            df['user_creation_time'] = pd.to_datetime(df['user_creation_time'])
        else:
            df = pd.read_sql_query(query, connection)

    return df


def fetch_data(query: str, dtype: bool = True) -> pd.DataFrame:
    USER, DATABASE, PASSWORD, HOST = check_env_vars()
    engine = create_engine(f"mysql://{USER}:{PASSWORD}@{HOST}:3306/{DATABASE}")
    if dtype:
        return pd.read_sql_query(query, engine,
                                 dtype=DTYPES, index_col='tweet_id')
    return pd.read_sql_query(query, engine)


def get_df_from_db(query_: str, path_: str = '', local = True) -> pd.DataFrame:
    if local == True:
        return get_local_data(query_,path_)
    else:
        return fetch_data(query_)


