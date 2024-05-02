import json
import os
from typing import List, Dict, Any


def look_for_tweet(tweet: Dict[str, Any], list_of_tweets: List[Dict[str, Any]]):
    """
    Recursively looks for a suitable tweet to reply to.
    :param tweet: the tweet that is to be appended to the replies list.
    :param list_of_tweets: the list of tweets to be looked into.
    :return: True if a suitable (reply) tweet is found, False otherwise.
    """
    for item in list_of_tweets:
        if item['id_str'] == tweet['in_reply_to_status_id_str']:
            item.setdefault('replies', []).append(tweet)  # setdefault sets the value if it doesn't exist yet
            return True
        elif 'replies' in item and look_for_tweet(tweet, item['replies']):
            return True
    return False


def add_tweet_to_replies(tweet: Dict[str, Any], list_of_tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Add the tweet to the reply array of another tweet (if found), otherwise append to the list of all tweets.
    :param tweet: the tweet to be added.
    :param list_of_tweets: the collection of tweets to look in.
    :return: the updated list of tweets.
    """
    if not look_for_tweet(tweet, list_of_tweets):  # if no suitable tweet was found
        list_of_tweets.append(tweet)
    return list_of_tweets


def process_tweets_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read and process tweets from a file.
    :param file_path: the path to the file to read from.
    :return: the list of tweets from the file.
    """
    cleaned_tweets: List[Dict[str, Any]] = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                tweet: Dict[str, Any] = json.loads(line.strip())
                cleaned_tweets = add_tweet_to_replies(tweet, cleaned_tweets)
            except Exception as e:
                print(f'{type(e)}: {e}.')
                continue

    return cleaned_tweets


def write_tweets_to_file(cleaned_tweets, output_filename) -> None:
    """
    Store the cleaned tweets in a file.
    :param cleaned_tweets: the JSON objects representing tweets.
    :param output_filename: the location to save in.
    :return: nothing.
    """
    with open(output_filename, 'w') as file:
        for tweet in cleaned_tweets:
            file.write(json.dumps(tweet) + '\n')


def delete_existing_file(file_path: str) -> None:
    """
    Deletes the file if it exists.
    :param file_path: the path to the file.
    :return: nothing.
    """
    file_path: str = fr'{file_path}'
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"'{file_path.split('/')[-1]}' was deleted.")


def start_creating_conversations(input_file_path: str) -> None:
    """
    Initializer function for conversation_threading.py
    :param input_file_path: the full path to the JSON file to create threads from.
    :return: nothing.
    """
    file_name: str = input_file_path.split("/")[-1]
    out_file_path: str = f'conversations/cleaned_{file_name}'

    cleaned_tweets = process_tweets_from_file(input_file_path)
    write_tweets_to_file(cleaned_tweets, out_file_path)
