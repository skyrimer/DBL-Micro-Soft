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


create_db("nezox2um_dbl", "nezox2um_dbl", "OX8tAkhwowXp", "nezox2um.beget.tech")
