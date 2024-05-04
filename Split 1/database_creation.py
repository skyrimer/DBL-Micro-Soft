from os import getenv
import mysql.connector
from mysql.connector import Error, InterfaceError, OperationalError
import json
from datetime import datetime
from tqdm import tqdm
import time


def connect_to_database(user_fill, database_fill, password_fill, host_fill):
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
    try:
        # Establish a connection to MySQL
        connection = connect_to_database(user, database, password, host)
    except Error as e:
        return e

    users = """ CREATE TABLE IF NOT EXISTS Users(
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

    tweets = """ CREATE TABLE IF NOT EXISTS Tweets(
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

    for data in batch_data:
        try:
            cursor.execute(insertion_user, data[1])
            cursor.execute(insertion_tweets, data[3])
        except (InterfaceError, OperationalError) as ex:
            print(f"Error inserting data: {ex}")
            cursor._cnx.rollback()
            raise
        except Exception as ex:
            print(f"Error inserting data: {ex}")
            cursor._cnx.rollback()
        else:
            cursor._cnx.commit()


def process_json_object(dict_):
    if 'delete' in dict_:
        return None

    user = dict_.get("user", {})

    text = dict_.get("full_text", dict_.get("text", ""))
    date_string = user.get("created_at", "")
    date_object = datetime.strptime(date_string, "%a %b %d %H:%M:%S %z %Y") if date_string else None
    timestamp = date_object.timestamp() if date_object else None

    user_id = user.get("id_str", "")
    location = user.get("location", "")
    verified = user.get("verified", False)
    followers_count = user.get("followers_count", 0)
    friends_count = user.get("friends_count", 0)
    statuses_count = user.get("statuses_count", 0)
    default_profile = int(user.get("default_profile", False))
    default_profile_image = int(user.get("default_profile_image", False))

    user_data = (user_id, location, verified, followers_count, friends_count,
                 statuses_count, timestamp, default_profile, default_profile_image)

    tweet_id = str(dict_['id_str'])
    lang = str(dict_.get('lang', 'en'))
    creation_time = int(dict_.get('timestamp_ms', '0')) // 1000
    country_code = None if dict_.get('place') is None else dict_["place"]["country_code"]
    favorite_count = int(dict_.get('favorite_count', 0))
    retweet_count = int(dict_.get('retweet_count', 0))
    source_link = str(dict_.get('source', ''))
    possibly_sensitive = int(dict_.get("possibly_sensitive", False))
    replied_tweet_id = str(dict_.get('in_reply_to_status_id_str'))
    replied_count = int(dict_.get('replied_count', 0))
    quoted_tweet_id = str(dict_.get('quoted_tweet_id_str'))
    quoted_count = int(dict_.get('quoted_count', 0))

    tweet_data = (tweet_id, user_id, text, lang, creation_time, country_code,
                  favorite_count, retweet_count, source_link, possibly_sensitive,
                  replied_tweet_id, replied_count,quoted_tweet_id, quoted_count)

    return ("Users", user_data, "Tweets", tweet_data)


def database_fill(user_fill: str, database_fill: str, password_fill: str, host_fill: str):
    batch_size = 500
    retries = 5
    delay = 1
    try:
        with open(r"C:\Users\20232075\PycharmProjects\DBL-Micro-Soft\Split 1\data\cleaned_tweets_combined.json",
                  'r') as file:
            file_content = file.read()
            json_objects = file_content.strip().split(",\n")

            total_iterations = len(json_objects)
            progress_bar = tqdm(total=total_iterations, desc="Processing")
            connection = connect_to_database(user_fill, database_fill, password_fill, host_fill)
            cursor = connection.cursor()
            batch_data = []
            for string in json_objects:
                try:
                    dict_ = json.loads(string)
                    data = process_json_object(dict_)
                    if data:
                        batch_data.append(data)
                    if len(batch_data) == batch_size:
                        insert_batch_with_retries(cursor, batch_data, retries, delay)
                        batch_data = []
                    progress_bar.update(1)
                except Error as ex:
                    print(f"Error processing record: {string}\nException: {ex}")
                    continue

            if batch_data:
                insert_batch_with_retries(cursor, batch_data, retries, delay)

            progress_bar.close()

    except (InterfaceError, OperationalError) as ex:
        print(f"Connection error: {ex}")
        if connection:
            connection.rollback()
    except Error as e:
        print(f"Error: {e}")
        return
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def insert_batch_with_retries(cursor, batch_data, retries, delay):
    for attempt in range(retries):
        try:
            insert_batch_data(cursor, batch_data)
            break
        except OperationalError as ex:
            print(f"Retry {attempt + 1}/{retries} failed: {ex}")
            time.sleep(delay)
            delay *= 2
        except InterfaceError as ex:
            print(f"Retry {attempt + 1}/{retries} failed: {ex}")
            cursor.connection = connect_to_database(
                cursor.connection.user, cursor.connection.database,
                cursor.connection.password, cursor.connection.server_host
            )
            delay *= 2
        except Exception as ex:
            print(f"Error inserting data: {ex}")
            break

if __name__ == "__main__":
    while True:
        try:
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

            print("Start database data insertion")
            database_fill("nezox2um_dbl", "nezox2um_dbl", "OX8tAkhwowXp", "nezox2um.beget.tech")
            print("Data insertion finished")

            break
        except Error as e:
            print(f"Retrying due to error: {e}")
            time.sleep(5)
