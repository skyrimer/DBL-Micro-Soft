from typing import List, Dict, Any

test_dict = {
    "created_at": "Wed May 22 12:20:55 +0000 2019",
    "id": 1131173091651072000,
    "id_str": "1131173091651072000",
    "text": "@BilalEksiTHY TK Elite Plus Helpdesk'e, Lufthansa ucuslarinda, Miles&amp;Smiles  statu mili kazan",
    "source": '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>',
    "truncated": True,
    "in_reply_to_status_id": None,
    "in_reply_to_status_id_str": None,
    "in_reply_to_user_id": 788882697955467266,
    "in_reply_to_user_id_str": "788882697955467266",
    "in_reply_to_screen_name": "BilalEksiTHY",
    "user": {
        "id": 58563850,
        "id_str": "58563850",
        "name": "Mustafa Kilicaslan",
        "screen_name": "Mustafakilicasl",
        "location": None,
        "url": None,
        "description": None,
        "translator_type": "none",
        "protected": False,
        "verified": False,
        "followers_count": 208,
        "friends_count": 755,
        "listed_count": 3,
        "favourites_count": 74,
        "statuses_count": 63,
        "created_at": "Mon Jul 20 19:25:01 +0000 2009",
        "utc_offset": None,
        "time_zone": None,
        "geo_enabled": False,
        "lang": None,
        "contributors_enabled": False,
        "is_translator": False,
        "profile_background_color": "131516",
        "profile_background_image_url": "http://abs.twimg.com/images/themes/theme14/bg.gif",
        "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme14/bg.gif",
        "profile_background_tile": True,
        "profile_link_color": "009999",
        "profile_sidebar_border_color": "EEEEEE",
        "profile_sidebar_fill_color": "EFEFEF",
        "profile_text_color": "333333",
        "profile_use_background_image": True,
        "profile_image_url": "http://pbs.twimg.com/profile_images/1536749913/4Y6H7532_normal.JPG",
        "profile_image_url_https": "https://pbs.twimg.com/profile_images/1536749913/4Y6H7532_normal.JPG",
        "default_profile": False,
        "default_profile_image": False,
        "following": None,
        "follow_request_sent": None,
        "notifications": None,
    },
    "geo": None,
    "coordinates": None,
    "place": None,
    "contributors": None,
    "is_quote_status": False,
    "extended_tweet": {
        "full_text": "@BilalEksiTHY TK Elite Plus Helpdesk'e, Lufthansa ucuslarinda, Miles&amp;Smiles",
        "display_text_range": [0, 275],
        "entities": {
            "hashtags": [],
            "urls": [],
            "user_mentions": [
                {
                    "screen_name": "BilalEksiTHY",
                    "name": "Bilal EKŞİ",
                    "id": 788882697955467266,
                    "id_str": "788882697955467266",
                    "indices": [0, 13],
                }
            ],
            "symbols": [],
        },
    },
    "quote_count": 0,
    "reply_count": 0,
    "retweet_count": 0,
    "favorite_count": 0,
    "entities": {
        "hashtags": [],
        "urls": [
            {
                "url": "https://t.co/f6eVSMhW1D",
                "expanded_url": "https://twitter.com/i/web/status/1131173091651072000",
                "display_url": "twitter.com/i/web/status/1…",
                "indices": [121, 144],
            }
        ],
        "user_mentions": [
            {
                "screen_name": "BilalEksiTHY",
                "name": "Bilal EKŞİ",
                "id": 788882697955467266,
                "id_str": "788882697955467266",
                "indices": [0, 13],
            }
        ],
        "symbols": [],
    },
    "favorited": False,
    "retweeted": False,
    "filter_level": "low",
    "lang": "tr",
    "timestamp_ms": "1558527655886",
}


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
        "quoted_status_permalink",
        "retweeted_status",
        "extended_entities",
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


def start_cleaning(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Initializer function for data_processing.py.
    :param dictionary: the original dictionary to process.
    :return: the processed dictionary.
    """
    return delete_unnecessary_keys(dictionary)
