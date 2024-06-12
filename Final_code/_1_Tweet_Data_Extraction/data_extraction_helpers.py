import json
import os
from typing import Any, Dict, List


def could_be_json(string: str) -> bool:
    """
    Checks if a given string could potentially represent a JSON object.

    Args:
        string (str): The input string to be checked.

    Returns:
        bool: True if the string could represent a JSON object, False otherwise.
    """
    return bool(string.startswith("{") and string.endswith("}"))


def delete_existing_file(file_path: str) -> None:
    """
    Deletes the file at the specified file path if it exists.

    Args:
        file_path (str): The path to the file to be deleted.

    Returns:
        None
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path.split('/')[-1]}' was deleted.")


def read_from_file(file_name: str) -> List[Dict[str, Any]]:
    """
    Reads JSON data from a file and returns a list of dictionaries representing the tweets.

    Args:
        file_name (str): The name of the file to read JSON data from.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the tweets read from the file.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        tweets_in_file: List[Dict[str, Any]] = []
        for line in file:
            line: str = line.strip().removesuffix(",")
            # do not consider anything that is not json
            if could_be_json(line):
                tweet: Dict[str, Any] = json.loads(line)
                tweets_in_file.append(tweet)
        return tweets_in_file


def start_cleaning(dictionary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Cleans and structures a dictionary representing user and tweet data.

    Args:
        dictionary (Dict[str, Any]): The dictionary containing user and tweet data.

    Returns:
        Dict[str, Dict[str, Any]]: A cleaned and structured dictionary
            with user and tweet dictionaries inside.
    """
    user: Dict[str, Any] = dictionary.get("user", {})
    country_code: str = "un"
    if place := dictionary.get("place"):
        country_code = place.get("country_code")

    clean_dict: Dict[str, Dict[str, Any]] = {
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

    text: str = ""
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
