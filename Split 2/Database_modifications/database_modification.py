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
add_tweet_sentiment_score = """ALTER TABLE Conversations ADD COLUMN category FLOAT;"""


add_conversations = """
CREATE TABLE IF NOT EXISTS Conversations(
conversation_id INTEGER,
tweet_order INTEGER,
tweet_id VARCHAR(20),
PRIMARY KEY (conversation_id, tweet_order),
FOREIGN KEY (tweet_id) REFERENCES Tweets(tweet_id)
)
"""


add_conversations_category  = """
CREATE TABLE IF NOT EXISTS ConversationsCategory (
conversation_id INTEGER PRIMARY KEY,
category VARCHAR(255),
confidence FLOAT,
FOREIGN KEY (conversation_id) REFERENCES Conversations(conversation_id)
);
"""



if __name__ == "__main__":
    connection: mysql.connector.connection.MySQLConnection = connect_to_database(
        user, database, password, host
    )
    with connection.cursor() as cursor:
        print("Start execution")
        cursor.execute(add_tweet_sentiment_score)
        cursor.execute(add_conversations)
        cursor.execute(add_conversations_category)
        connection.commit()
        print("End execution")
        
