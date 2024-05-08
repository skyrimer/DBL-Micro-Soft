import json
import os
from typing import List, Dict, Any
from data_processing import start_cleaning
from data_extraction import delete_existing_file
from tqdm.auto import tqdm

current_directory: str = os.getcwd()

all_tweet_id: set = set()


def could_be_json(string: str) -> bool:
    """
    Checks if a given string could potentially be a JSON object based on its format.
    :param string:Input string to check.
    :return: True if the string could be a JSON object, False otherwise.
    """
    return bool(string.startswith("{") and string.endswith("}"))


def read_from_file(file_name: str) -> List[Dict[str, Any]]:
    """
    Reads and cleans tweets from a JSON file.
    :param file_name: the path to the file.
    :return: the list of tweets (dictionaries) in the file.
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


def append_to_file(tweets_list: List[Dict[str, Any]]) -> None:
    """
    Appends a list of tweets in JSON format to a file.
    :param tweets_list: List of dictionaries representing tweets to append.
    :return: None.
    """
    output_file_path: str = os.path.join(
        current_directory, "data", "cleaned_tweets_combined.json"
    )
    with open(output_file_path, "a", encoding="utf-8") as file:
        for tweet in tweets_list:
            if not valid_tweet(tweet):
                continue
            file.write(json.dumps(tweet) + ",\n")
            all_tweet_id.add(tweet["tweet"]["tweet_id"])


def valid_tweet(tweet: Dict[str, Any]) -> bool:
    """
    Check if a tweet is valid.

    Args:
        tweet (dict): A dictionary containing tweet and user information.
    Returns:
        bool: True if the tweet realistic, False otherwise.
    """

    return all(
        [
            tweet["tweet"]["tweet_id"],
            tweet["user"]["user_id"],
            tweet["tweet"]["tweet_id"] not in all_tweet_id,
            tweet["user"]["followers_count"] >= 0,
            tweet["user"]["friends_count"] >= 0,
            tweet["user"]["statuses_count"] >= 0,
        ]
    )


def start_general_extraction(sample_data_only: bool = True) -> None:
    """
    Initializer function for general_data_extraction.py
    :param sample_data_only: defines which dataset to extract from.
    :return: nothing.
    """
    # Resets output file
    output_file_path: str = os.path.join(
        current_directory, "data", "cleaned_tweets_combined.json"
    )
    delete_existing_file(output_file_path)

    # Extract all tweets from files, append them to the output file
    json_folder: str = "data" if sample_data_only else "all_data"
    path_to_all_json_files: str = os.path.join(current_directory, json_folder)

    all_raw_json_files: List[str] = os.listdir(path_to_all_json_files)
    for file in tqdm(all_raw_json_files, mininterval=1):  # noqa
        # old backup
        if file == "all_clean_tweets.json":
            continue
        tweets_from_file: List[Dict[str, Any]] = read_from_file(
            os.path.join(path_to_all_json_files, file)
        )
        cleaned_tweets_list = []
        for tweet in tweets_from_file:
            if quote := tweet.get("quoted_status"):
                cleaned_tweets_list.append(start_cleaning(quote, "quote"))
            if original_tweet := tweet.get("retweeted_status"):
                cleaned_tweets_list.extend(
                    (
                        start_cleaning(original_tweet, "tweet"),
                        start_cleaning(tweet, "retweet"),
                    )
                )
            else:
                cleaned_tweets_list.append(start_cleaning(tweet, "tweet"))
        append_to_file(cleaned_tweets_list)  # noqa
