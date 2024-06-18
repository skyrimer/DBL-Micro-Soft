import json
import os
import sqlite3
from typing import List, Tuple, Any

from tqdm.auto import tqdm

from Final_code._2_Insert_Tweets_to_Database.helper_functions import process_json_object
from Final_code._0_Constants.defined_paths import path_processed_tweets_json


def create_db_sqllite3(file_name: str) -> None:
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


def insert_batch_data_sqlite3(cursor: sqlite3.Cursor, batch_data: List[Tuple[Tuple[Any, ...], Tuple[Any, ...]]]) -> None:
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


def database_fill_sqllite3(database_path: str):
    batch_size = 100_000
    with open(
        path_processed_tweets_json,
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


if __name__ == "__main__":
    database_name = "local_backup.db"
    database_path = os.path.join("../Local_Database", database_name)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    if os.path.exists(database_path):
        print("Start dropping database")
        os.remove(database_path)
        print("End dropping database")
    print("Start local database creation")
    create_db_sqllite3(database_path)
    print("Local database has been created")
    print("Start local database data insertion")
    database_fill_sqllite3(database_path)
    print("Local data insertion finished")
