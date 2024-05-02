from os import getenv
import mysql.connector
from mysql.connector import Error


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
    try:
        # Establish a connection to MySQL
        connection = mysql.connector.connect(
            user=user,
            database=database,
            password=password,
            host=host,
        )
    except Error as e:
        return e

    users = """ CREATE TABLE IF NOT EXISTS Users(
            user_id VARCHAR(255) PRIMARY KEY,
            country_code VARCHAR(255),
            verified TINYINT NOT NULL,
            followers_count BIGINT NOT NULL,
            friends_count BIGINT NOT NULL,
            listed_count BIGINT NOT NULL,
            statuses_count BIGINT NOT NULL,
            favourites_count BIGINT NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            defaul_profile TINYINT NOT NULL,
            default_profile_image TINYINT NOT NULL            
        );"""

    tweets = """ CREATE TABLE IF NOT EXISTS Tweets(
            tweet_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            full_text VARCHAR(65535) NOT NULL,
            lang VARCHAR(255) NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            place_full_name VARCHAR(255) NOT NULL,
            favorite_count INT NOT NULL,
            retweet_count INT NOT NULL,
            source_name VARCHAR(255) NOT NULL,
            country_code VARCHAR(10),
            possibly_sensitive TINYINT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );"""

    replies = """
        CREATE TABLE IF NOT EXISTS Replies(
            tweet_id VARCHAR(255) PRIMARY KEY,
            replied_tweet_id VARCHAR(255) NOT NULL,
            reply_count BIGINT NOT NULL,
            FOREIGN KEY (tweet_id) REFERENCES Tweets(tweet_id) ON DELETE CASCADE
        );"""

    quotes = """
        CREATE TABLE IF NOT EXISTS Quotes(
            tweet_id VARCHAR(255) PRIMARY KEY,
            quoted_status_id VARCHAR(255) NOT NULL,
            quote_count BIGINT NOT NULL,
            FOREIGN KEY (tweet_id) REFERENCES Tweets(tweet_id) ON DELETE CASCADE
        );"""

    cursor = connection.cursor()
    cursor.execute(users)
    cursor.execute(tweets)
    cursor.execute(replies)
    cursor.execute(quotes)
    connection.close()


if __name__ == "__main__":
    user = getenv("DBL_USER")
    assert (
        user is not None
    ), "DBL_USER is required but not found in environment variables"

    database = getenv("DBL_DATABASE")
    assert (
        database is not None
    ), "DBL_DATABASE is required but not found in environment variables"

    password = getenv("DBL_PASSWORD")
    assert (
        password is not None
    ), "DBL_PASSWORD is required but not found in environment variables"

    host = getenv("DBL_HOST")
    assert (
        host is not None
    ), "DBL_HOST is required but not found in environment variables"

    print("Start database creation on the server")
    create_db(user, database, password, host)
    print("Database has been created")
