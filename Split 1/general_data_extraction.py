import json
import os
from typing import List, Dict, Any
from data_processing import start_cleaning
from data_extraction import delete_existing_file


def read_from_file(file_name: str) -> List[Dict[str, Any]]:
    """
    Reads and cleans tweets from a JSON file.
    :param file_name: the path to the file.
    :return: the list of tweets (dictionaries) in the file.
    """
    with open(file_name, 'r') as file:
        tweets_in_file: List[Dict[str, Any]] = []
        for line in file:
            tweet: Dict[str, Any] = json.loads(line)
            tweets_in_file.append(tweet)

        return tweets_in_file


def append_to_file(tweet: Dict[str, Any]) -> None:
    output_file_path: str = os.getcwd() + '/data/' + 'cleaned_tweets_combined.json'
    with open(output_file_path, 'a', encoding='utf-8') as file:
        file.write(json.dumps(tweet) + '\n')


def start_general_extraction(sample_data_only: bool = True) -> None:
    """
    Initializer function for general_data_extraction.py
    :param sample_data_only: defines which dataset to extract from.
    :return: nothing.
    """
    # Resets output file
    output_file_path: str = os.getcwd() + '/data/' + 'cleaned_tweets_combined.json'
    delete_existing_file(output_file_path)

    # Extract all tweets from files, append them to the output file
    if sample_data_only:
        path_to_all_json_files: str = os.getcwd() + '/data/'
    else:
        # Move all data given for the challenge to this directory before running
        path_to_all_json_files: str = os.getcwd() + '/all_data/'
    all_raw_json_files: List[str] = os.listdir(path_to_all_json_files)
    for file in all_raw_json_files:
        tweets_from_file: List[Dict[str, Any]] = read_from_file(path_to_all_json_files + file)
        for tweet in tweets_from_file:
            cleaned_tweet: Dict[str, Any] = start_cleaning(tweet)
            append_to_file(cleaned_tweet)
