import json
import os
from typing import Any, Dict, List


def could_be_json(string: str) -> bool:
    """
    Checks if a given string could potentially be a JSON object based on its format.
    :param string:Input string to check.
    :return: True if the string could be a JSON object, False otherwise.
    """
    return bool(string.startswith("{") and string.endswith("}"))


def delete_existing_file(file_path: str) -> None:
    """
    Deletes a file if it exists.
    :param file_path: the path to the file.
    :return: nothing.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path.split('/')[-1]}' was deleted.")


def read_from_file(file_name: str) -> List[Dict[str, Any]]:
    """
    Reads and processes tweets from a JSON file.

    This function opens the specified JSON file and then checks for each line if it could be a valid
    JSON object. If it is, the function converts it into a dictionary, and appends it to a list of tweets.

    :param file_name: The path to the JSON file containing tweet data.
    :return: A list of dictionaries, where each dictionary represents a tweet.
    """
    with open(file_name, "r") as file:
        tweets_in_file: List[Dict[str, Any]] = []
        for line in file:
            line: str = line.strip().removesuffix(",")
            # do not consider anything that is not json
            if could_be_json(line):
                tweet: Dict[str, Any] = json.loads(line)
                tweets_in_file.append(tweet)
        return tweets_in_file

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

