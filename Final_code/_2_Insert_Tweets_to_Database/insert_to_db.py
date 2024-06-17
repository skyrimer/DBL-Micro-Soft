import json
import os
import sys
from typing import Any, Dict, List, Tuple

from helper_functions import process_json_object
from tqdm.auto import tqdm

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "_0_Constants_and_Utils",
    )
)

from database_queries import *
from database_utils import connect_to_database, execute_queries, form_connection_params
from defined_paths import path_processed_tweets_json


def create_db(connection_params: Dict[str, Any], local: bool) -> None:
    """
    Creates database tables for storing user and tweet data based on the connection parameters and database type.

    Args:
        connection_params (Dict[str, Any]): The parameters required to establish a database connection.
        local (bool): Flag indicating whether the database is local (SQLite) or remote (MySQL).

    Returns:
        None
    """
    connection = connect_to_database(connection_params, local)
    table_creation: List[str] = [
        CREATE_USERS_MYSQL,
        CREATE_TWEETS_MYSQL,
        CREATE_CONVERSATIONS_MYSQL,
        CREATE_CONVERSATIONS_CATEGORY_MYSQL,
    ]
    if local:
        table_creation: List[str] = [
            CREATE_USERS_SQLITE,
            CREATE_TWEETS_SQLITE,
            CREATE_CONVERSATIONS_SQLITE,
            CREATE_CONVERSATIONS_CATEGORY_SQLITE,
        ]

    execute_queries(connection, table_creation)
    connection.close()


def database_fill(
    connection_params: Dict[str, Any], local: bool, batch_size: int
) -> None:
    """
    Fills the database tables with user and tweet data in batches.

    Args:
        connection_params (Dict[str, Any]): The parameters required to establish a database connection.
        local (bool): Flag indicating whether the database is local (SQLite) or remote (MySQL).
        batch_size (int): The size of each batch for data insertion.

    Returns:
        None
    """
    insertion_user: str = """
    INSERT OR IGNORE INTO Users(user_id, verified, followers_count, friends_count,
    statuses_count, creation_time, default_profile, default_profile_image)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?);
    """

    insertion_tweets: str = """
    INSERT OR IGNORE INTO Tweets(tweet_id, user_id, full_text, lang, creation_time, country_code, favorite_count,
    retweet_count, possibly_sensitive, replied_tweet_id, reply_count, quoted_status_id, quote_count)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    if not local:
        insertion_user = insertion_user.replace("?", "%s").replace(" OR", "")
        insertion_tweets = insertion_tweets.replace("?", "%s").replace(" OR", "")

    with open(path_processed_tweets_json, "r") as file:
        connection = connect_to_database(connection_params, local)
        user_data: List[Tuple[Any, ...]] = []
        tweet_data: List[Tuple[Any, ...]] = []
        for line in tqdm(file, desc="Uploading data: ", mininterval=5):
            tweet_dict: Dict[str, Any] = json.loads(line[:-2])
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
    local: bool = True
    reset: bool = False
    batch_size: int = 100_000
    connection_params: Dict[str, Any] = form_connection_params(local)
    if reset:
        print("Resetting the database")
        connection = connect_to_database(connection_params, local)
        execute_queries(
            connection,
            [
                "DROP TABLE IF EXISTS ConversationsCategory",
                "DROP TABLE IF EXISTS Conversations",
                "DROP TABLE IF EXISTS Tweets",
                "DROP TABLE IF EXISTS Users",
            ],
        )
    print("Start database creation")
    create_db(connection_params, local)
    print("Database has been created")
    print("Start data insertion")
    database_fill(connection_params, local, batch_size)
    print("Data insertion finished")
