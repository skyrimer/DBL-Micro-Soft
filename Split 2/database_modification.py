from os import getenv

import mysql.connector


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


user, database, password, host = (
    getenv("DBL_USER"),
    getenv("DBL_DATABASE"),
    getenv("DBL_PASSWORD"),
    getenv("DBL_HOST"),
)

# Update the tweets table to have the semantic analysis score
add_tweet_sentiment_score = """ALTER TABLE Tweets ADD COLUMN sentiment_score FLOAT;"""


add_tweet_estimation = """CREATE TABLE IF NOT EXISTS Conversations (
    first_tweet_id VARCHAR(20) NOT NULL,
    last_tweet_id VARCHAR(20) NOT NULL,
    conversation TEXT NOT NULL,
    PRIMARY KEY (first_tweet_id, last_tweet_id)
);"""


if __name__ == "__main__":
    connection: mysql.connector.connection.MySQLConnection = connect_to_database(
        user, database, password, host
    )
    with connection.cursor() as cursor:
        print("Start execution")
        cursor.execute(add_tweet_sentiment_score)
        cursor.execute(add_tweet_estimation)
        print("End execution")
