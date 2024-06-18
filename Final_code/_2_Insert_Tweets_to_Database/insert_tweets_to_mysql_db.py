import json
import os
import sys
from typing import Any, List, Tuple

import mysql
from helper_functions import process_json_object
from tqdm.auto import tqdm


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from defined_paths import path_processed_tweets_json
from env_vars import check_env_vars


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


def insert_batch_data(
    cursor: mysql.connector.cursor.MySQLCursor,
    batch_data: List[Tuple[Tuple[Any, ...], Tuple[Any, ...]]],
) -> None:
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


def database_fill(
    user_fill: str, database_fill: str, password_fill: str, host_fill: str
):
    batch_size = 10_000
    with open(
        path_processed_tweets_json,
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


if __name__ == "__main__":
    user, database, password, host = check_env_vars()
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
