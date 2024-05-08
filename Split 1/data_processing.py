from typing import List, Dict, Any
from datetime import datetime


def delete_nested_key(item: Dict[str, Any], key: str) -> Dict[str, Any]:
    """
    Recursively iterates over a nested key and removes the deepest key and its value. Updates the passed dictionary.
    :param item: the dictionary to remove the nested key from.
    :param key: the nested key to remove.
    :return: the dictionary with the specified key returned.
    """
    nested_keys: List[str] = key.split(".", 1)
    parent_key: str = nested_keys[0]
    child_key: str = nested_keys[1]

    # Recursion if the key is nested with 2+ levels (2+ dots in it)
    if "." in child_key and parent_key in item:
        item[parent_key] = delete_nested_key(item[parent_key], child_key)
    if (
        parent_key in item
        and item[parent_key] is not None
        and child_key in item[parent_key].keys()
    ):
        del item[parent_key][child_key]  # Deletes the deepest key

    return item


def delete_unnecessary_keys(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deletes a list of unnecessary (nested) keys from a dictionary.
    :param item: the original dictionary to be cleaned.
    :return: the cleaned dictionary.
    """

    # A list of irrelevant keys to remove. Keys with a dot (".") represent nested keys.
    keys_to_remove: List[str] = [
        "created_at",
        "id",
        "truncated",
        "display_text_range",
        "in_reply_to_status_id",
        "in_reply_to_user_id",
        "in_reply_to_user_id_str",
        "in_reply_to_screen_name",
        "user.name",
        "user.screen_name",
        "user.id",
        "user.url",
        "user.description",
        "user.utc_offset",
        "user.time_zone",
        "user.geo_enabled",
        "user.lang",
        "user.contributors_enabled",
        "user.is_translator",
        "user.profile_background_color",
        "user.profile_background_image_url",
        "user.profile_background_image_url_https",
        "user.profile_background_tile",
        "user.profile_link_color",
        "user.profile_sidebar_border_color",
        "user.profile_sidebar_fill_color",
        "user.profile_text_color",
        "user.profile_use_background_image",
        "user.profile_image_url",
        "user.profile_image_url_https",
        "user.profile_banner_url",
        "user.follow_request_sent",
        "user.notifications",
        "user.translator_type",
        "user.protected",
        "user.listed_count",
        "user.favourites_count",
        "user.following",
        "extended_tweet.display_text_range",
        "extended_tweet.entities",
        "extended_tweet.extended_entities",
        "entities",
        "quoted_status_id",
        "quoted_status",
        "favorited",
        "coordinates",
        "place.attributes",
        "place.bounding_box",
        "place.country",
        "place.full_name",
        "place.id",
        "place.name",
        "place.place_type",
        "place.url",
        "retweeted",
        "filter_level",
        "matching_rules",
        "geo",
        "contributors",
        "is_quote_status",
        "retweeted_status",
        "quoted_status_permalink",
        "retweeted_status",
        "extended_entities",
        "user.location",
    ]
    for key in keys_to_remove:
        # Remove non-nested keys instantly
        if key in item.keys():
            del item[key]
        # Call a function to remove (multi-)nested keys.
        elif "." in key:
            item: Dict[str, Any] = delete_nested_key(item, key)

    return item


def print_readable_dict(item: dict, indent: int = 0) -> None:
    """
    Recursively prints a dictionary in a readable format.
    :param item: the dictionary to print.
    :param indent: the indentation level (4 spaces = 1 tab).
    :return: nothing.
    """
    for key, value in item.items():
        if isinstance(value, dict):
            print(" " * indent + f"\033[1m{key}:\033[0m")  # Keys will be bold
            print_readable_dict(value, indent + 4)
        else:
            print(" " * indent + f"\033[1m{key}:\033[0m {value}")  # Keys will be bold


def start_cleaning(dictionary: Dict[str, Any], category: str) -> Dict[str, Any]:
    """
    Initializer function for data_processing.py.
    :param dictionary: the original dictionary to process.
    :return: the processed dictionary.
    """
    user = dictionary.get("user", {})
    country_code = ""
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
        "lang": dictionary.get("lang"),
        "creation_time": dictionary.get("created_at"),
        "country_code": country_code,
        "favorite_count": dictionary.get("favorite_count", 0),
        "retweet_count": dictionary.get("retweet_count", 0),
        "possibly_sensitive": dictionary.get("possibly_sensitive", False),
        "replied_tweet_id": dictionary.get("in_reply_to_status_id_str"),
        "replied_count": dictionary.get("replied_count", 0),
        "quoted_status_id": dictionary.get("quoted_status_id"),
        "quoted_count": dictionary.get("quoted_count", 0),
        "category": category,
    }
    return clean_dict
