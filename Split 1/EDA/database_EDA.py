from sqlalchemy import create_engine
import pandas as pd


def database_read(db_username, db_password, db_host, db_port, db_name):
    """
    This function connects to a MySQL database and retrieves data from the Users and Tweets tables.

    Args:
        db_username (str): the username for the MySQL database
        db_password (str): the password for the MySQL database
        db_host (str): the hostname or IP address of the MySQL database
        db_port (str): the port number for the MySQL database
        db_name (str): the name of the MySQL database

    Returns:
        pd.DataFrame: a Pandas DataFrame containing the data from the Users and Tweets tables
    """

    engine = create_engine(
        f'mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

    # Add columns in SELECT to retrieve data from the Users and Tweets tables
    query = """
    SELECT u.user_id, u.location, u.friends_count, t.full_text, t.lang
    FROM Users u
    JOIN Tweets t ON u.user_id = t.user_id
    GROUP BY u.user_id
    """

    df = pd.read_sql(query, engine)
    return df


# Unsafe, but did not have to time to set environment variables
db_username = "nezox2um_dbl"
db_password = 'OX8tAkhwowXp'
db_host = "nezox2um.beget.tech"
db_port = '3306'
db_name = 'nezox2um_dbl'


df = database_read(db_username, db_password, db_host, db_port, db_name)
print(df.head())
print(df.describe(include="all"))
missing_values_per_column = df.isna().sum()
print("Missing values per column:")
print(missing_values_per_column)
