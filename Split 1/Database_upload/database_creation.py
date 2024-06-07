# import mysql.connector
import json
import os
import sqlite3
from datetime import datetime
from os import getenv

import mysql
from tqdm.auto import tqdm


def connect_to_database(
    user_fill: str, database_fill: str, password_fill: str, host_fill: str
):
    """
    Connect to a database using the provided credentials.

    Args:
        user_fill (str): The username for the database connection.
        database_fill (str): The name of the database to connect to.
        password_fill (str): The password for the database user.
        host_fill (str): The host address of the database.

    Returns:
        mysql.connector.connection.MySQLConnection: A connection to the database.

    """
    return mysql.connector.connect(
        user=user_fill,
        database=database_fill,
        password=password_fill,
        host=host_fill,
        connect_timeout=10,
    )


def create_db(user: str, database: str, password: str, host: str) -> None:
    """
    Creates a MySQL database with tables for Users, Tweets, Replies, and Quotes.

    Args:
        user: MySQL user.
        database: Name of the database to connect.
        password: Password for the MySQL user.
        # host: Host address of the MySQL server.

    Returns:
        None if successful, Error object if connection or table creation fails.
    """
    connection = connect_to_database(user, database, password, host)

    users: str = """ CREATE TABLE IF NOT EXISTS Users(
            user_id VARCHAR(20) PRIMARY KEY,
            verified TINYINT NOT NULL,
            followers_count INT NOT NULL,
            friends_count INT NOT NULL,
            statuses_count INT NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            default_profile TINYINT(1) NOT NULL,
            default_profile_image TINYINT(1) NOT NULL            
        );"""

    tweets: str = """ CREATE TABLE IF NOT EXISTS Tweets(
            tweet_id VARCHAR(20) PRIMARY KEY,
            user_id VARCHAR(20) NOT NULL,
            full_text TEXT NOT NULL,
            lang CHAR(2) NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            country_code VARCHAR(2),
            favorite_count INT NOT NULL,
            retweet_count INT NOT NULL,
            possibly_sensitive TINYINT(1),
            replied_tweet_id VARCHAR(20),
            reply_count INT NOT NULL,
            quoted_status_id VARCHAR(20),
            quote_count INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );"""

    cursor = connection.cursor()
    cursor.execute(users)
    cursor.execute(tweets)
    cursor.close()


def create_db_sqllite3(file_name) -> None:
    connection = sqlite3.connect(file_name)
    cursor = connection.cursor()

    users: str = """ CREATE TABLE IF NOT EXISTS Users(
            user_id TEXT PRIMARY KEY,
            verified INTEGER NOT NULL,
            followers_count INTEGER NOT NULL,
            friends_count INTEGER NOT NULL,
            statuses_count INTEGER NOT NULL,
            creation_time BLOB NOT NULL,
            default_profile INTEGER NOT NULL,
            default_profile_image INTEGER NOT NULL            
        );"""

    tweets: str = """ CREATE TABLE IF NOT EXISTS Tweets(
            tweet_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            full_text TEXT NOT NULL,
            lang TEXT NOT NULL,
            creation_time BLOB NOT NULL,
            country_code TEXT,
            favorite_count INT NOT NULL,
            retweet_count INT NOT NULL,
            possibly_sensitive INT,
            replied_tweet_id TEXT,
            reply_count INT NOT NULL,
            quoted_status_id TEXT,
            quote_count INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );"""

    cursor.execute(users)
    cursor.execute(tweets)
    cursor.close()


def insert_batch_data(cursor, batch_data):
    """
    Inserts batch data into Users and Tweets tables.

    Args:
        cursor: Database cursor to execute SQL queries.
        batch_data: List of tuples containing user and tweet data to be inserted.

    Returns:
        None
    """
    if not batch_data:
        return

    insertion_user = """
    INSERT IGNORE INTO Users(user_id, verified, followers_count, friends_count,
    statuses_count, creation_time, default_profile, default_profile_image)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
    """

    insertion_tweets = """
    INSERT INTO Tweets(tweet_id, user_id, full_text, lang, creation_time, country_code, favorite_count,
    retweet_count, possibly_sensitive, replied_tweet_id, reply_count, quoted_status_id, quote_count)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    user_data = []
    tweet_data = []
    for data in batch_data:
        user_data.append(data[0])
        tweet_data.append(data[1])

    cursor.executemany(insertion_user, user_data)
    cursor.executemany(insertion_tweets, tweet_data)
    cursor._cnx.commit()


def insert_batch_data_sqlite3(cursor, batch_data):
    """
    Inserts batch data into Users and Tweets tables.

    Args:
        cursor: Database cursor to execute SQL queries.
        batch_data: List of tuples containing user and tweet data to be inserted.

    Returns:
        None
    """
    if not batch_data:
        return

    insertion_user = """
    INSERT OR IGNORE INTO Users(user_id, verified, followers_count, friends_count,
    statuses_count, creation_time, default_profile, default_profile_image)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?);
    """

    insertion_tweets = """
    INSERT INTO Tweets(tweet_id, user_id, full_text, lang, creation_time, country_code, favorite_count,
    retweet_count, possibly_sensitive, replied_tweet_id, reply_count, quoted_status_id, quote_count)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    user_data = []
    tweet_data = []
    for data in batch_data:
        user_data.append(data[0])
        tweet_data.append(data[1])

    cursor.executemany(insertion_user, user_data)
    cursor.executemany(insertion_tweets, tweet_data)
    cursor.connection.commit()


def process_json_object(dict_):
    """
    Processes a JSON object to extract user and tweet data.

    Args:
        dict_: Dictionary representing a JSON object containing user and tweet information.

    Returns:
        Tuple containing user data and tweet data extracted from the JSON object.
    """

    user = dict_["user"]
    tweet = dict_["tweet"]

    user_data = (
        user["user_id"],
        user["verified"],
        user["followers_count"],
        user["friends_count"],
        user["statuses_count"],
        (
            datetime.strptime(user["created_at"], "%a %b %d %H:%M:%S %z %Y")
            if user["created_at"]
            else 0
        ),
        user["default_profile"],
        user["default_profile_image"],
    )

    tweet_data = (
        tweet["tweet_id"],
        user["user_id"],
        tweet["text"],
        tweet["lang"],
        (
            datetime.strptime(tweet["creation_time"], "%a %b %d %H:%M:%S %z %Y")
            if tweet["creation_time"]
            else 0
        ),
        tweet["country_code"],
        tweet["favorite_count"],
        tweet["retweet_count"],
        tweet["possibly_sensitive"],
        tweet["replied_tweet_id"],
        tweet["reply_count"],
        tweet["quoted_status_id"],
        tweet["quote_count"],
    )
    return (user_data, tweet_data)


def database_fill(
    user_fill: str, database_fill: str, password_fill: str, host_fill: str
):
    batch_size = 10_000
    with open(
        os.path.join("data_processed", "cleaned_tweets_combined.json"),
        "r",
    ) as file:
        connection = connect_to_database(
            user_fill, database_fill, password_fill, host_fill
        )
        cursor = connection.cursor()
        batch_data = []
        for line in tqdm(file, desc="Processing", mininterval=5):
            tweet_dict = json.loads(line[:-2])
            if data := process_json_object(tweet_dict):
                batch_data.append(data)
            if len(batch_data) >= batch_size:
                insert_batch_data(cursor, batch_data)
                batch_data = []
        if batch_data:
            insert_batch_data(cursor, batch_data)
    cursor.close()
    connection.close()


def database_fill_sqllite3(database_path: str):
    batch_size = 100_000
    with open(
        os.path.join("data_processed", "cleaned_tweets_combined.json"),
        "r",
    ) as file:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        batch_data = []
        for line in tqdm(file, desc="Processing", mininterval=5):
            tweet_dict = json.loads(line[:-2])
            if data := process_json_object(tweet_dict):
                batch_data.append(data)
            if len(batch_data) >= batch_size:
                insert_batch_data_sqlite3(cursor, batch_data)
                batch_data = []
        if batch_data:
            insert_batch_data_sqlite3(cursor, batch_data)
    cursor.close()
    connection.close()


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

    env_var = getenv(env_var_str)
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


if __name__ == "__main__":
    # user, database = "nezox2um_test", "nezox2um_test"
    drop_database = True
    local_database = True
    if local_database:
        database_name = "local_backup.db"
        database_path = os.path.join("data_processed", database_name)
        if drop_database and os.path.exists(database_path):
            print("Start dropping database")
            os.remove(database_path)
            print("End dropping database")
        print("Start local database creation")
        create_db_sqllite3(database_path)
        print("Local database has been created")
        print("Start local database data insertion")
        database_fill_sqllite3(database_path)
        print("Local data insertion finished")
    else:
        user, database, password, host = check_env_vars()
        if drop_database:
            print("Start dropping database")
            connection = connect_to_database(user, database, password, host)
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS Tweets")
            cursor.execute("DROP TABLE IF EXISTS Users")
            cursor.close()
            connection.close()
            print("End dropping database")
        print("Start database creation on the server")
        create_db(user, database, password, host)
        print("Database has been created")
        print("Start database data insertion")
        database_fill(user, database, password, host)
        print("Data insertion finished")
