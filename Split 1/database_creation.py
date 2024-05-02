import mysql.connector
from mysql.connector import Error


def create_db(user: str, database: str, password: str, host: str):
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

    users = """
        CREATE TABLE IF NOT EXISTS users(
            user_id BIGINT PRIMARY KEY,
            location VARCHAR(50),
            verified TINYINT NOT NULL,
            followers_count BIGINT NOT NULL,
            friends_count BIGINT NOT NULL,
            listed_count BIGINT NOT NULL,
            favourites_count BIGINT NOT NULL,
            statuses_count BIGINT NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            protected BOOL NOT NULL
        );
        """

    tweets = """
        CREATE TABLE IF NOT EXISTS tweets(
            tweet_id BIGINT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            text VARCHAR(65535) NOT NULL,
            lang VARCHAR(30) NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            place_full_name VARCHAR(50) NOT NULL,
            favorite_count INT NOT NULL,
            retweet_count INT NOT NULL
        );
        """

    replies = """
        CREATE TABLE IF NOT EXISTS replies(
            tweet_id BIGINT PRIMARY KEY,
            replied_tweet_id BIGINT NOT NULL,
            reply_count BIGINT NOT NULL
        );
        """

    quotes = """
        CREATE TABLE IF NOT EXISTS quotes(
            tweet_id INT PRIMARY KEY,
            quoted_status_id BIGINT NOT NULL,
            quote_count INT NOT NULL
        );
        """

    hashtags = """
        CREATE TABLE IF NOT EXISTS hashtags(
            hashtag_id BIGINT PRIMARY KEY AUTO_INCREMENT,
            tweet_id BIGINT NOT NULL,
            hashtag VARCHAR(60) NOT NULL
        );
        """

    cursor = connection.cursor()
    cursor.execute(users)
    cursor.execute(tweets)
    cursor.execute(replies)
    cursor.execute(quotes)
    cursor.execute(hashtags)
    connection.close()


create_db("nezox2um_dbl", "nezox2um_dbl", "OX8tAkhwowXp", "nezox2um.beget.tech")
