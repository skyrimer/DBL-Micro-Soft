import json
import os
import sys
from typing import Any, Dict, List, Set

from data_extraction_helpers import delete_existing_file, read_from_file, start_cleaning
from tqdm.auto import tqdm

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "_0_Constants_and_Utils",
    )
)

from defined_paths import folder_path_processed, path_processed_tweets_json


def append_to_file(tweets_list: List[Dict[str, Any]], output_file_path: str) -> None:
    """
    Appends a list of tweet dictionaries to a file in JSON format.

    Args:
        tweets_list (List[Dict[str, Any]]): The list of tweet dictionaries to append to the file.
        output_file_path (str): The path to the output file.

    Returns:
        None
    """
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
        tweet (Dict[str, Any]): A dictionary containing tweet and user information.

    Returns:
        bool: True if the tweet is valid, False otherwise.
    """
    return all(
        [
            tweet["tweet"]["tweet_id"],
            tweet["tweet"]["tweet_id"] not in all_tweet_id,
            tweet["user"]["user_id"],
            tweet["user"]["followers_count"] >= 0,
            tweet["user"]["friends_count"] >= 0,
            tweet["user"]["statuses_count"] >= 0,
        ]
    )


def start_general_extraction() -> None:
    """
    Initializes the tweet extraction and cleaning process.

    This function performs the following tasks:
    1. Resets the output file where the cleaned tweets will be stored.
    2. Iterates through all raw JSON tweet files in the specified directory.
    3. Reads tweets from each file, processes them, and cleans them.
    4. Appends the cleaned tweets to the output file.

    The folder with the JSON files to be cleaned must be in the same
    directory as this file, under the name 'data_raw'.

    The cleaned data will be in the directory of this project, under
    /data_processed/cleaned_tweets_combined.json.
    """
    output_file_path: str = path_processed_tweets_json

    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Resets output file
    delete_existing_file(output_file_path)

    # Extract all tweets from files, append them to the output file
    path_to_all_json_files: str = os.path.join(folder_path_processed, "data_raw")

    all_raw_json_files: List[str] = os.listdir(path_to_all_json_files)
    for file in tqdm(
        all_raw_json_files,
        bar_format="Processing files: {n_fmt}/{total_fmt} ({percentage:.0f}%) [Elapsed: {elapsed}, Remaining: {remaining}, {rate_fmt}]",
    ):
        tweets_from_file: List[Dict[str, Any]] = read_from_file(
            os.path.join(path_to_all_json_files, file)
        )
        cleaned_tweets_list: List[Dict[str, Dict[str, Any]]] = []
        for tweet in tweets_from_file:
            if quote := tweet.get("quoted_status"):
                cleaned_tweets_list.append(start_cleaning(quote))
            if original_tweet := tweet.get("retweeted_status"):
                cleaned_tweets_list.extend(
                    (
                        start_cleaning(original_tweet),
                        start_cleaning(tweet),
                    )
                )
            else:
                cleaned_tweets_list.append(start_cleaning(tweet))
        append_to_file(cleaned_tweets_list, output_file_path)


if __name__ == "__main__":
    all_tweet_id: Set[str] = set()
    start_general_extraction()
