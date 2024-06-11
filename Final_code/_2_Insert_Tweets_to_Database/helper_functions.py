from datetime import datetime
from typing import Dict, Any

def process_json_object(dict_: Dict[str, Dict[str, Any]]) -> tuple[tuple[Any]]:
    """
    Processes a dictionary containing user and tweet data and extracts relevant information for database insertion.
    
    Args:
        dict_ (Dict[str, Dict[str, Any]]): The dictionary containing user and tweet data.
    
    Returns:
        tuple[tuple[Any]]: A tuple of tuples containing processed user and tweet data for database insertion.
    """

    user = dict_["user"]
    tweet = dict_["tweet"]

    user_data = (
        user["user_id"],
        user["verified"],
        user["followers_count"],
        user["friends_count"],
        user["statuses_count"],
        (
            datetime.strptime(user["created_at"], "%a %b %d %H:%M:%S %z %Y")
            if user["created_at"]
            else 0
        ),
        user["default_profile"],
        user["default_profile_image"],
    )

    tweet_data = (
        tweet["tweet_id"],
        user["user_id"],
        tweet["text"],
        tweet["lang"],
        (
            datetime.strptime(tweet["creation_time"], "%a %b %d %H:%M:%S %z %Y")
            if tweet["creation_time"]
            else 0
        ),
        tweet["country_code"],
        tweet["favorite_count"],
        tweet["retweet_count"],
        tweet["possibly_sensitive"],
        tweet["replied_tweet_id"],
        tweet["reply_count"],
        tweet["quoted_status_id"],
        tweet["quote_count"],
    )
    return (user_data, tweet_data)
