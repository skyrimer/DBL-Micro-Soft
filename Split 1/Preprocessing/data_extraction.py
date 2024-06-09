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
    Deletes the JSON file of the company if it exists.
    :param file_path: the path to the file.
    :return: nothing.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path.split('/')[-1]}' was deleted.")


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



