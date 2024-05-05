from os import getenv
import os
import mysql.connector
from mysql.connector import Error, InterfaceError, OperationalError
import json
from datetime import datetime
from tqdm import tqdm
import time


# TODO: count connect disconnect
def connect_to_database(
    user_fill: str, database_fill: str, password_fill: str, host_fill: str
) -> mysql.connector.connection.MySQLConnection:
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
        connect_timeout=5,
    )


def create_db(user: str, database: str, password: str, host: str) -> None:
    """
    Creates a MySQL database with tables for Users, Tweets, Replies, and Quotes.

    Args:
        user: MySQL user.
        database: Name of the database to connect.
        password: Password for the MySQL user.
        host: Host address of the MySQL server.

    Returns:
        None if successful, Error object if connection or table creation fails.
    """
    connection: mysql.connector.connection.MySQLConnection = connect_to_database(
        user, database, password, host
    )

    users: str = """ CREATE TABLE IF NOT EXISTS Users(
            user_id VARCHAR(255) PRIMARY KEY,
            location VARCHAR(255),
            verified TINYINT NOT NULL,
            followers_count INT NOT NULL,
            friends_count INT NOT NULL,
            statuses_count INT NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            default_profile TINYINT NOT NULL,
            default_profile_image TINYINT NOT NULL            
        );"""

    tweets: str = """ CREATE TABLE IF NOT EXISTS Tweets(
            tweet_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            full_text VARCHAR(255) NOT NULL,
            lang VARCHAR(281) NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            country_code VARCHAR(255),
            favorite_count INT NOT NULL,
            retweet_count INT NOT NULL,
            source_link VARCHAR(255),
            possibly_sensitive TINYINT,
            replied_tweet_id VARCHAR(255),
            reply_count INT NOT NULL,
            quoted_status_id VARCHAR(255),
            quote_count INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );"""

    cursor = connection.cursor()
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
    INSERT IGNORE INTO Users(user_id, location, verified, followers_count, friends_count,
    statuses_count, creation_time, default_profile, default_profile_image)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    insertion_tweets = """
    INSERT INTO Tweets(tweet_id, user_id, full_text, lang, creation_time, country_code, favorite_count,
    retweet_count, source_link, possibly_sensitive, replied_tweet_id, reply_count, quoted_status_id, quote_count)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    user_data = []
    tweet_data = []
    for data in batch_data:
        user_data.append(data[0])
        tweet_data.append(data[1])

    cursor.executemany(insertion_user, user_data)
    cursor.executemany(insertion_tweets, tweet_data)
    cursor._cnx.commit()


def process_json_object(dict_):
    """
    Processes a JSON object to extract user and tweet data.

    Args:
        dict_: Dictionary representing a JSON object containing user and tweet information.

    Returns:
        Tuple containing user data and tweet data extracted from the JSON object.
    """

    if "delete" in dict_:
        return None

    user = dict_.get("user", {})

    text = dict_.get(
        "full_text", dict_.get("text", "")
    )  # TODO: what do we do with empty text???
    date_string = user.get("created_at", "")
    date_object = (
        datetime.strptime(date_string, "%a %b %d %H:%M:%S %z %Y")
        if date_string
        else None
    )
    timestamp = date_object.timestamp() if date_object else None

    user_id = user.get("id_str", "")
    location = user.get("location", "")
    verified = user.get("verified", False)
    followers_count = user.get("followers_count", 0)
    friends_count = user.get("friends_count", 0)
    statuses_count = user.get("statuses_count", 0)
    default_profile = int(user.get("default_profile", True))
    default_profile_image = int(user.get("default_profile_image", True))

    user_data = (
        user_id,
        location,
        verified,
        followers_count,
        friends_count,
        statuses_count,
        timestamp,
        default_profile,
        default_profile_image,
    )

    tweet_id = dict_["id_str"]
    lang = dict_.get("lang", "en")
    creation_time = int(dict_.get("timestamp_ms", 0)) // 1000
    country_code = (
        None if dict_.get("place") is None else dict_["place"]["country_code"]
    )
    favorite_count = dict_.get("favorite_count", 0)
    retweet_count = dict_.get("retweet_count", 0)
    source_link = dict_.get("source", "")
    possibly_sensitive = dict_.get("possibly_sensitive", False)
    replied_tweet_id = dict_.get("in_reply_to_status_id_str")
    replied_count = dict_.get("replied_count", 0)
    quoted_tweet_id = dict_.get("quoted_tweet_id_str")
    quoted_count = dict_.get("quoted_count", 0)

    tweet_data = (
        tweet_id,
        user_id,
        text,
        lang,
        creation_time,
        country_code,
        favorite_count,
        retweet_count,
        source_link,
        possibly_sensitive,
        replied_tweet_id,
        replied_count,
        quoted_tweet_id,
        quoted_count,
    )

    return (user_data, tweet_data)


def database_fill(
    user_fill: str, database_fill: str, password_fill: str, host_fill: str
):
    batch_size = 1000
    with open(
        os.path.join(os.getcwd(), "data", "cleaned_tweets_combined.json"),
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
            if len(batch_data) == batch_size:
                insert_batch_data(cursor, batch_data)
                batch_data = []
        if batch_data:
            insert_batch_data(cursor, batch_data)
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
    user, database, password, host = check_env_vars()
    print("Start database creation on the server")
    create_db(user, database, password, host)
    print("Database has been created")
    print("Start database data insertion")
    database_fill(user, database, password, host)
    print("Data insertion finished")
