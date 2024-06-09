from typing import Any, Dict, List


def start_cleaning(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Initializer function for data_processing.py.
    :param dictionary: the original dictionary to process.
    :return: the processed dictionary.
    """
    user = dictionary.get("user", {})
    country_code = "un"
    if place := dictionary.get("place"):
        country_code = place.get("country_code")

    clean_dict = {
        "user": {
            "user_id": user.get("id_str"),
            "verified": user.get("verified", False),
            "followers_count": max(user.get("followers_count", 0), 0),
            "friends_count": max(user.get("friends_count", 0), 0),
            "statuses_count": max(user.get("statuses_count", 0), 0),
            "created_at": user.get("created_at"),
            "default_profile": int(user.get("default_profile", True)),
            "default_profile_image": int(user.get("default_profile_image", True)),
        }
    }
    if extended_tweet := dictionary.get("extended_tweet"):
        text = extended_tweet.get("full_text", dictionary.get("text", ""))
    else:
        text = dictionary.get("text", "")
    clean_dict["tweet"] = {
        "tweet_id": dictionary.get("id_str"),
        "text": text,
        "lang": dictionary.get("lang", "un"),
        "creation_time": dictionary.get("created_at"),
        "country_code": country_code,
        "favorite_count": dictionary.get("favorite_count", 0),
        "retweet_count": dictionary.get("retweet_count", 0),
        "reply_count": dictionary.get("reply_count", 0),
        "possibly_sensitive": dictionary.get("possibly_sensitive", False),
        "replied_tweet_id": dictionary.get("in_reply_to_status_id_str"),
        "replied_count": dictionary.get("replied_count", 0),
        "quoted_status_id": dictionary.get("quoted_status_id"),
        "quote_count": dictionary.get("quote_count", 0),
    }
    return clean_dict
