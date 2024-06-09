
# This is a file with constants used for visualizations

QUERY_ALL = """
SELECT 
    Users.user_id AS user_id, 
    Users.creation_time AS user_creation_time, 
    Users.verified,
    Users.followers_count,
    Users.friends_count,
    Users.statuses_count,
    Users.default_profile,
    Users.default_profile_image,
    Tweets.creation_time AS tweet_creation_time,
    Tweets.tweet_id,
    Tweets.full_text,
    Tweets.lang,
    Tweets.country_code,
    Tweets.favorite_count,
    Tweets.retweet_count,
    Tweets.possibly_sensitive,
    Tweets.replied_tweet_id,
    Tweets.reply_count,
    Tweets.quoted_status_id,
    Tweets.quote_count
FROM Users
INNER JOIN Tweets ON Users.user_id = Tweets.user_id;
"""

QUERY_REPLY = """
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

DTYPES = {
"user_id": "object",
"user_creation_time": "datetime64[ns]",
"verified": "bool",
"followers_count": "int32",
"friends_count": "int32",
"statuses_count": "int32",
"default_profile": "bool",
"default_profile_image": "bool",
"tweet_creation_time": "datetime64[ns]",
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

COMPANY_NAME_TO_ID = {
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

COMPANY_ID_TO_NAME = {v: k for k, v in COMPANY_NAME_TO_ID.items()}