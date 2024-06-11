import json
import os
import sys

from helper_functions import process_json_object
from tqdm.auto import tqdm

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_0_Constants_and_Utils"))

from database_utils import connect_to_database, execute_queries, form_connection_params
from defined_paths import path_processed_tweets_json


def create_db(connection_params: dict, local: bool) -> None:
    """
    Creates database tables for storing user and tweet data based on the connection parameters and database type.

    Args:
        connection_params (dict): The parameters required to establish a database connection.
        local (bool): Flag indicating whether the database is local (SQLite) or remote (MySQL).

    Returns:
        None
    """

    connection = connect_to_database(connection_params, local)
    if local:
        create_users: str = """ CREATE TABLE IF NOT EXISTS Users(
                user_id TEXT PRIMARY KEY,
                verified INTEGER NOT NULL,
                followers_count INTEGER NOT NULL,
                friends_count INTEGER NOT NULL,
                statuses_count INTEGER NOT NULL,
                creation_time BLOB NOT NULL,
                default_profile INTEGER NOT NULL,
                default_profile_image INTEGER NOT NULL            
            );"""

        create_tweets: str = """ CREATE TABLE IF NOT EXISTS Tweets(
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
    else:
        create_users: str = """ CREATE TABLE IF NOT EXISTS Users(
            user_id VARCHAR(20) PRIMARY KEY,
            verified TINYINT NOT NULL,
            followers_count INT NOT NULL,
            friends_count INT NOT NULL,
            statuses_count INT NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            default_profile TINYINT(1) NOT NULL,
            default_profile_image TINYINT(1) NOT NULL            
        );"""

        create_tweets: str = """ CREATE TABLE IF NOT EXISTS Tweets(
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
    execute_queries(connection, [create_users, create_tweets])
    connection.close()


def database_fill(connection_params: dict, local: bool, batch_size: int) -> None:
    """
    Fills the database tables with user and tweet data in batches.

    Args:
        connection_params (dict): The parameters required to establish a database connection.
        local (bool): Flag indicating whether the database is local (SQLite) or remote (MySQL).
        batch_size (int): The size of each batch for data insertion.

    Returns:
        None
    """

    insertion_user = """
    INSERT OR IGNORE INTO Users(user_id, verified, followers_count, friends_count,
    statuses_count, creation_time, default_profile, default_profile_image)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?);
    """

    insertion_tweets = """
    INSERT OR IGNORE INTO Tweets(tweet_id, user_id, full_text, lang, creation_time, country_code, favorite_count,
    retweet_count, possibly_sensitive, replied_tweet_id, reply_count, quoted_status_id, quote_count)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    if not local:
        insertion_user = insertion_user.replace("?", "%s").replace(" OR", "")
        insertion_tweets = insertion_tweets.replace("?", "%s").replace(" OR", "")

    print()
    print()
    print()
    print(insertion_user)
    print(insertion_tweets)

    with open(path_processed_tweets_json, "r") as file:
        connection = connect_to_database(connection_params, local)
        user_data, tweet_data = [], []
        for line in tqdm(file, desc="Uploading data: ", mininterval=5):
            tweet_dict = json.loads(line[:-2])
            if data := process_json_object(tweet_dict):
                user_data.append(data[0])
                tweet_data.append(data[1])
            if len(user_data) >= batch_size:
                execute_queries(
                    connection,
                    [(insertion_user, user_data), (insertion_tweets, tweet_data)],
                )
                user_data, tweet_data = [], []
        if user_data:
            execute_queries(
                connection,
                [(insertion_user, user_data), (insertion_tweets, tweet_data)],
            )

        connection.close()


if __name__ == "__main__":
    local = False
    reset = True
    batch_size = 100_000
    connection_params = form_connection_params(local)
    if reset:
        print("Resetting the database")
        connection = connect_to_database(connection_params, local)
        execute_queries(
            connection,
            [
                "DROP TABLE IF EXISTS Tweets",
                "DROP TABLE IF EXISTS Users",
                "DROP TABLE IF EXISTS Conversations",
                "DROP TABLE IF EXISTS ConversationsCategories",
            ],
        )
    print("Start local database creation")
    create_db(connection_params, local)
    print("Local database has been created")
    print("Start local database data insertion")
    database_fill(connection_params, local, batch_size)
    print("Local data insertion finished")
