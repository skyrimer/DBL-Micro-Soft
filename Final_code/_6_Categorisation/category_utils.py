import re
import string
from functools import lru_cache
from typing import List

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Initialize once to avoid repeated initialization
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


@lru_cache(maxsize=512)
def process_token(token):
    return lemmatizer.lemmatize(token) if token not in stop_words else ""


def normalise_text(tweet):
    # Convert to lowercase
    tweet = tweet.lower()
    # Removing RT indication
    tweet = re.sub(r"^rt ", "", tweet)
    # Remove URLs
    tweet = re.sub(r"http\S+|www\S+|https\S+", "", tweet, flags=re.MULTILINE)
    # Remove user mentions
    tweet = re.sub(r"@\w+", "", tweet)
    # Remove hashtag symbols but keep the words
    tweet = re.sub(r"#", "", tweet)
    # Remove punctuation
    tweet = tweet.translate(str.maketrans("", "", string.punctuation))
    # Remove numbers
    tweet = re.sub(r"\d+", "", tweet)
    # Tokenize the tweet
    tokens = word_tokenize(tweet)
    # Process tokens to remove stop words and lemmatize
    processed_tokens = [process_token(token) for token in tokens if token]
    # Join the tokens back into a single string
    return " ".join(processed_tokens).strip()


def get_batches(df: pd.DataFrame, batch_size: int = 1000) -> List[pd.DataFrame]:
    return [df.iloc[i : i + batch_size] for i in range(0, len(df), batch_size)]


def convert_to_list(df: pd.DataFrame) -> List[List]:
    # Ensure the index contains the conversation IDs as native Python int
    conversation_ids = df.index.to_list()  # Convert to list of native Python int
    # Convert categories to strings
    categories = df["category"].astype(str).to_list()  # Convert to list of str
    # Combine the conversation IDs and categories into a list of tuples
    return list(zip(categories, conversation_ids))
