import json
import os
from typing import List

data_directory: str = r"/data/"
current_directory: str = os.getcwd()


def lufthansa_related(tweet: str) -> bool:
    """
    Checks if the tweet is related to Lufthansa.
    :param tweet: the string item of the tweet.
    :return: True if related to Lufthansa, False otherwise.
    """
    if "124476322" in tweet or "lufthansa" in tweet or "Lufthansa" in tweet:
        return True
    return False


def list_files() -> List[str]:
    """
    Gets all files from a directory.
    :return: the list of files from the directory.
    """
    files_list: List[str] = []
    files: List[str] = os.listdir(current_directory+data_directory)
    for file in files:
        files_list.append(file)
    return files_list


def read_file(file_name: str) -> List[str]:
    """
    Reads data (tweets) from the json file.
    :param file_name: the file to read from.
    :return: data to append to the output file.
    """
    data_to_append: List[str] = []
    with open(current_directory+data_directory+file_name, 'r') as file:
        file_content: str = file.read()
        json_objects: List[str] = file_content.strip().split('\n')
        for item in json_objects:
            try:
                if lufthansa_related(item):
                    luft_tweet = json.loads(item)
                    data_to_append.append(luft_tweet)
            except Exception as e:
                continue
    return data_to_append


def write_to_file(data: List[str]) -> None:
    """
    Writes data to the output file.
    :param data: information to write to the file.
    :return: nothing.
    """
    with open(fr"{current_directory}/airlines/lufthansa.json", 'a', encoding='utf-8') as file:
        for string in data:
            file.write(str(string) + '\n')


files_in_root = list_files()
for json_file in files_in_root:
    tweet_info = read_file(json_file)
    write_to_file(tweet_info)
