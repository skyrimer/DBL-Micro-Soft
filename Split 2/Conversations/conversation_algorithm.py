from collections import defaultdict
from tqdm.notebook import tqdm
import pandas as pd

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, conversation):
        node = self.root
        for tweet_id in conversation:
            node = node.children[tweet_id]
        node.is_end = True

    def is_subset(self, conversation):
        node = self.root
        for tweet_id in conversation:
            if tweet_id not in node.children:
                return False
            node = node.children[tweet_id]
        return True

def trace_conversation(start_tweet_id: str, tweet_dict: dict):
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
        users_in_conversation.add(tweet_info['user_id'])
        local_processed_tweet_ids.add(current_tweet_id)
        if len(users_in_conversation) > 2:
            return convo[:-1][::-1], users_in_conversation  # As soon as the third user appears, we delete his tweet and return
        current_tweet_id = tweet_info['replied_tweet_id']
    return (convo[::-1], users_in_conversation) if len(users_in_conversation) == 2 else (None, users_in_conversation)

def extract_conversations(df: pd.DataFrame, user_ids: list):
    df.index = df.index.astype(str)
    tweet_dict = df.to_dict('index')
    conversations = []
    trie = Trie()  # Initialize trie for subset checks
    user_ids_set = set(user_ids)  # Convert list to set for faster membership checking

    # Start tracing conversations from tweets that are replies
    for tweet_id in tqdm(df[df['replied_tweet_id'].notnull()].index, desc="Extracting all conversations"):
        conversation, users_in_conversation = trace_conversation(tweet_id, tweet_dict)
        if conversation and user_ids_set.intersection(users_in_conversation) and not trie.is_subset(conversation):
            trie.insert(conversation)
            conversations.append(conversation)

    return conversations