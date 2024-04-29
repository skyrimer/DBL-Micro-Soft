import sqlite3
import os

name = "aviation.db"


def establish_connection(db_path):
    """
    Establishes and returns a database connection to the SQLite database specified by db_path.

    Args:
    db_path (str): The path to the database file.

    Returns:
    sqlite3.Connection: A connection object to the SQLite database.
    """
    connection = sqlite3.connect(db_path)
    return connection


# TODO check database 1 more time
def build_db(db_path):
    """
    Creates necessary tables in the database to store tweets, users, replies, retweets,
   quotes, hashtags, mentions, and symbols. Each table is created only if it does not already exist.

   Args:
   db_path (str): The path to the database file.
   """
    # TODO udali nahui
    tweets = """
        CREATE TABLE IF NOT EXISTS tweets(
            tweet_id INT PRIMARY KEY,
            user_id INT NOT NULL,
            text TEXT NOT NULL,
            lang TEXT NOT NULL,
            tweet_type TEXT NOT NULL,
            creation_time INT NOT NULL,
            country TEXT NOT NULL,
            full_name TEXT NOT NULL,
            favorite_count INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """
    # TODO 1_or_0
    users = """
        CREATE TABLE IF NOT EXISTS users(
            user_id INT PRIMARY KEY,
            location TEXT,
            verified INT NOT NULL,
            followers_count INT NOT NULL,
            friends_count INT NOT NULL,
            listed_count INT NOT NULL, 
            favourites_count INT NOT NULL,
            statuses_count INT NOT NULL,
            creation_time INT NOT NULL
        );
        """

    replies = """
        CREATE TABLE IF NOT EXISTS replies(
            tweet_id INT PRIMARY KEY,
            replied_tweet_id INT NOT NULL,
            replied_user_id INT NOT NULL,
            reply_count INT NOT NULL,
            FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
        );
        """

    retweets = """
        CREATE TABLE IF NOT EXISTS retweets(
            tweet_id INT PRIMARY KEY,
            retweet_of_status_id INT NOT NULL,
            retweet_count INT NOT NULL,
            FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
        );
        """

    quotes = """
        CREATE TABLE IF NOT EXISTS quotes(
            tweet_id INT PRIMARY KEY,
            quoted_status INT NOT NULL,
            quote_count INT NOT NULL,
            FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
        );
        """

    hashtags = """
        CREATE TABLE IF NOT EXISTS hashtags(
            hashtag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id INT NOT NULL,
            hashtag TEXT NOT NULL,
            FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
        );
        """
    mentions = """
        CREATE TABLE IF NOT EXISTS user_mentions(
            user_mention_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id INT NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
        );
        """
    symbols = """
        CREATE TABLE IF NOT EXISTS symbols(
            symbol_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id INT NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
        );
        """
    conn = establish_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(tweets)
    cursor.execute(users)
    cursor.execute(replies)
    cursor.execute(retweets)
    cursor.execute(quotes)
    cursor.execute(hashtags)
    cursor.execute(mentions)
    cursor.execute(symbols)
    conn.close()


build_db(name)
