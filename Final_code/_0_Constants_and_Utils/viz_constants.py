from typing import Dict

# This is a file with constants used for visualizations

# SQL Queries
QUERY_REPLY: str = """
SELECT 
    t1.tweet_id AS tweet_id,
    t1.creation_time AS tweet_creation_time,
    t1.user_id AS user_id,
    t2.tweet_id AS original_tweet_id,
    t2.creation_time AS original_tweet_creation_time,
    t2.user_id AS original_user_id
FROM 
    Tweets t1
INNER JOIN 
    Tweets t2
ON 
    t1.replied_tweet_id = t2.tweet_id;
"""

QUERY_TWEETS: str = "SELECT * from Tweets"
QUERY_USERS: str = "SELECT * from Users"
QUERY_CONVERSATIONS: str = "SELECT * from Conversations"
QUERY_CONVERSATIONS_CATEGORY: str = "SELECT * from ConversationsCategory"

# Optimal dtypes
DTYPES_TWEETS: Dict[str, str] = {
    "creation_time": "datetime64[ns]",
    "tweet_id": "object",
    "full_text": "object",
    "lang": "category",
    "country_code": "category",
    "favorite_count": "int32",
    "retweet_count": "int32",
    "possibly_sensitive": "bool",
    "replied_tweet_id": "object",
    "reply_count": "int32",
    "quoted_status_id": "object",
    "quote_count": "int32",
}

DTYPES_USERS: Dict[str, str] = {
    "user_id": "object",
    "creation_time": "datetime64[ns]",
    "verified": "bool",
    "followers_count": "int32",
    "friends_count": "int32",
    "statuses_count": "int32",
    "default_profile": "bool",
    "default_profile_image": "bool",
}

DTYPES_CONVERSATIONS: Dict[str, str] = {
    "conversation_id": "int32",
    "tweet_order": "int16",
    "tweet_id": "object",
}

DTYPES_CONVERSATIONS_CATEGORY: Dict[str, str] = {
    "conversation_id": "int32",
    "category": "category",
}

# Airline specific info
COMPANY_NAME_TO_ID: Dict[str, str] = {
    "Klm": "56377143",
    "Air France": "106062176",
    "British Airways": "18332190",
    "American Air": "22536055",
    "Lufthansa": "124476322",
    "Air Berlin": "26223583",
    "Air Berlin assist": "2182373406",
    "easyJet": "38676903",
    "Ryanair": "1542862735",
    "Singapore Airlines": "253340062",
    "Qantas": "218730857",
    "Etihad Airways": "45621423",
    "Virgin Atlantic": "20626359",
}

COMPANY_ID_TO_NAME: Dict[str, str] = {v: k for k, v in COMPANY_NAME_TO_ID.items()}
