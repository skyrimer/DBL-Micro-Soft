from collections import defaultdict

import pandas as pd
from tqdm.notebook import tqdm


class TrieNode:
    """
    Trie node used in Trie data structure for efficient string storage and retrieval.
    """

    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end = False


class Trie:
    """
    Trie data structure for efficient storage and retrieval of conversations.

    Methods:
        insert(conversation): Inserts a conversation into the trie.
        is_subset(conversation): Checks if a conversation is a subset of existing conversations in the trie.
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, conversation):
        """
        Inserts a conversation into the trie.

        Args:
            conversation (list): List of tweet IDs representing a conversation to be inserted.
        """

        node = self.root
        for tweet_id in conversation:
            node = node.children[tweet_id]
        node.is_end = True

    def is_subset(self, conversation):
        """
        Checks if a conversation is a subset of existing conversations in the trie.

        Args:
            conversation (list): List of tweet IDs representing a conversation to check.

        Returns:
            bool: True if the conversation is a subset, False otherwise.
        """

        node = self.root
        for tweet_id in conversation:
            if tweet_id not in node.children:
                return False
            node = node.children[tweet_id]
        return True


def trace_conversation(start_tweet_id: str, tweet_dict: dict):
    """
    Trace a conversation starting from a given tweet ID in a dictionary of tweets.

    Args:
        start_tweet_id (str): The ID of the starting tweet.
        tweet_dict (dict): A dictionary containing tweet IDs as keys
            and tweet information as values.

    Returns:
        tuple: A tuple containing either the reversed conversation IDs
            and users involved if 3 users are present, or None and users
            involved if less than 3 users are present.
    """

    convo = []
    current_tweet_id = start_tweet_id
    users_in_conversation = set()
    local_processed_tweet_ids = set()  # Local set to track the current conversation
    while (
        current_tweet_id
        and current_tweet_id in tweet_dict
        and current_tweet_id not in local_processed_tweet_ids
    ):
        tweet_info = tweet_dict[current_tweet_id]
        convo.append(current_tweet_id)
        local_processed_tweet_ids.add(current_tweet_id)
        users_in_conversation.add(tweet_info["user_id"])
        if len(users_in_conversation) > 2:
            users_in_conversation.remove(tweet_info["user_id"])
            return (
                convo[:-1][::-1],
                users_in_conversation,
            )
        current_tweet_id = tweet_info["replied_tweet_id"]
    return (
        (convo[::-1], users_in_conversation)
        if len(users_in_conversation) == 2
        else (None, users_in_conversation)
    )


def extract_conversations(df: pd.DataFrame, user_ids: list):
    """
    Extract conversations from a DataFrame of tweets involving specified user IDs.

    Args:
        df (pd.DataFrame): DataFrame containing tweet information.
        user_ids (list): List of user IDs to filter conversations.

    Returns:
        list: A list of conversations extracted from the DataFrame
            based on the specified user IDs.
    """
    df.index = df.index.astype(str)
    tweet_dict = df.to_dict("index")
    conversations = []
    user_involved = []
    trie = Trie()  # Initialize trie for subset checks
    user_ids_set = set(user_ids)  # Convert list to set for faster membership checking

    # Start tracing conversations from tweets that are replies
    for tweet_id in tqdm(
        df[df["replied_tweet_id"].notnull()].index, desc="Extracting conversations: "
    ):
        conversation, users_in_conversation = trace_conversation(tweet_id, tweet_dict)
        if (
            conversation
            and user_ids_set.intersection(users_in_conversation)
            and not trie.is_subset(conversation)
        ):
            trie.insert(conversation)
            conversations.append(conversation)
            user_involved.append(users_in_conversation)

    return conversations
