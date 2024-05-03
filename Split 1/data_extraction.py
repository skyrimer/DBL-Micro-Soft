import json
import os
from typing import List, Dict, Any
from data_processing import start_cleaning
from conversation_threading import start_creating_conversations

data_directory: str = r"/data/"
current_directory: str = os.getcwd()
company_ids: Dict[str, str] = {
    "klm": "56377143",
    "airfrance": "106062176",
    "british_airways": "18332190",
    "americanair": "22536055",
    "lufthansa": "124476322",
    "airberlin": "26223583",
    "airberlin_assist": "2182373406",
    "easyjet": "38676903",
    "ryanair": "1542862735",
    "singaporeair": "253340062",
    "qantas": "218730857",
    "etihadairways": "45621423",
    "virginatlantic": "20626359",
}


def company_related(tweet: str, company_name: str) -> bool:
    """
    Checks if the tweet is related to a given company.
    :param tweet: the string item of the tweet and its metadata.
    :param company_name: the company name to check.
    :return: True if related, False otherwise.
    """
    return company_name in tweet or company_ids[company_name] in tweet


def list_files() -> List[str]:
    """
    Gets all files from a directory.
    :return: the list of files from the directory.
    """
    files_list: List[str] = os.listdir(current_directory + data_directory)
    return files_list


def read_file(file_name: str) -> Dict[str, List[Any]]:
    """
    Reads data (tweets) from the json file.
    :param file_name: the file to read from.
    :return: data to append to the output file.
    """

    # Tweets related to each company in the file
    data_to_append: Dict[str, List[Any]] = {
        "lufthansa": [],
        "klm": [],
        "airfrance": [],
        "british_airways": [],
        "americanair": [],
        "airberlin": [],
        "airberlin_assist": [],
        "easyjet": [],
        "ryanair": [],
        "singaporeair": [],
        "qantas": [],
        "etihadairways": [],
        "virginatlantic": [],
    }

    with open(current_directory + data_directory + file_name, "r") as file:
        file_content: str = file.read()
        json_objects: List[str] = file_content.strip().split("\n")
        for tweet in json_objects:
            try:
                for company_name in company_ids.keys():
                    if company_related(tweet.lower(), company_name):
                        item: Dict[str, Any] = json.loads(
                            tweet
                        )  # Converts from string to dictionary.
                        processed_item: Dict[str, Any] = start_cleaning(item)
                        data_to_append[company_name].append(processed_item)
            except json.JSONDecodeError as e:
                print(f"{type(e)}: {e}.")
    return data_to_append


def write_to_file(data: List[Any], company_name: str) -> None:
    """
    Writes company tweets to the output file.
    :param data: tweets metadata written to the file.
    :param company_name: the name of the company related to the tweets.
    :return: nothing.
    """
    file_path: str = rf"{current_directory}/airlines/{company_name}.json"
    with open(file_path, "a", encoding="utf-8") as file:
        for item in data:
            file.write(json.dumps(item) + "\n")


def delete_existing_file(file_path: str) -> None:
    """
    Deletes the JSON file of the company if it exists.
    :param file_path: the path to the file.
    :return: nothing.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path.split('/')[-1]}' was deleted.")


def start_extraction() -> None:
    """
    Initializer function for data_extraction.py
    :return: nothing.
    """
    # Resets the files to prevent duplicate data
    for company_name in company_ids.keys():
        company_file_path: str = rf"{os.getcwd()}/airlines/{company_name}.json"
        delete_existing_file(company_file_path)

    # Distributes tweets to JSON files for different companies
    files_in_root: List[str] = list_files()
    for json_file in files_in_root:
        tweets: Dict[str, List[Any]] = read_file(json_file)
        for company_name in tweets:
            write_to_file(tweets[company_name], company_name)

    # Creates conversation threads for each company
    path_to_company_data: str = f"{os.getcwd()}/airlines/"
    files_list: List[str] = os.listdir(path_to_company_data)
    files_list.remove(
        "_lufthansa.json"
    )  # Only for my local file, not necessary otherwise
    for json_file in files_list:
        start_creating_conversations(path_to_company_data + json_file)
