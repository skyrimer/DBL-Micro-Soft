import contextlib
import gc
import os
import re
import string
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

import pandas as pd
import tensorflow as tf
from scipy.special import softmax
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "_0_Constants_and_Utils",
    )
)

from database_utils import connect_to_database, execute_queries

# Load the tokenizer and model
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForSequenceClassification.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment"
)
if physical_devices := tf.config.list_physical_devices("GPU"):
    try:
        for device in physical_devices:
            tf.config.experimental.set_memory_growth(device, True)
    except RuntimeError as e:
        print(e)

device = "/GPU:0" if tf.config.list_physical_devices("GPU") else "/CPU:0"


def process_batch(texts):
    """
    Apply sentiment analysis to a batch of texts using a pre-trained transformer model.

    Parameters:
    texts (list): A list of texts to analyze.

    Returns:
    list: A list of ranked sentiment labels for the input texts.

    This function uses a pre-trained transformer model for sequence classification to analyze the sentiment of the texts in the given batch. It returns a list of ranked sentiment labels for the input texts, where the first label is the most likely sentiment and the subsequent labels are less likely sentiments.
    """
    # Get the maximum sequence length for the model
    encoded_input = tokenizer(
        texts, return_tensors="tf", padding=True, truncation=True, max_length=512
    )
    with tf.device(device):
        output = model(encoded_input)

    scores = output[0].numpy()
    scores = softmax(scores, axis=1)

    sentiment_scores = scores[:, 2] - scores[:, 0]
    return sentiment_scores.tolist()


def clear_gpu_memory():
    tf.keras.backend.clear_session()  # Clear the current session
    with contextlib.suppress(AttributeError):
        tf.compat.v1.reset_default_graph()  # For TensorFlow 1.x compatibility
    gc.collect()  # Explicitly call the garbage collector


def apply_sentiment_analysis(
    df: pd.DataFrame, text_column: str, batch_size=128, max_workers=4
):
    """
    Apply sentiment analysis to the given DataFrame using a pre-trained transformer model.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the text column to analyze.
    text_column (str): The name of the column in the DataFrame containing the text to analyze.
    batch_size (int): The number of texts to process in each batch. Default is 128.
    max_workers (int): The maximum number of worker threads to use for parallel processing. Default is 4.

    Returns:
    pd.DataFrame: The input DataFrame with an additional 'sentiment' column containing the sentiment analysis results.

    This function uses a pre-trained transformer model for sequence classification
    to analyze the sentiment of the texts in the given DataFrame. It applies the
    sentiment analysis in parallel using multiple worker threads to improve performance.
    The results are then added to the input DataFrame as a new 'sentiment' column.
    """
    texts = df[text_column].tolist()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            results.extend(executor.submit(process_batch, batch).result())
            clear_gpu_memory()
    df["sentiment"] = results
    return df


def clean_mentions(tweet):
    # Remove RT since it has no meaning
    tweet = re.sub(r"^RT ", "", tweet)
    # Remove URLs since they should not impact anything
    tweet = re.sub(r"http\S+|www\S+|https\S+", "", tweet)
    # Remove user mentions
    tweet = re.sub(r"@\w+", "", tweet)
    # Remove hashtag symbols but keep the words
    tweet = re.sub(r"#", "", tweet)
    # Remove unnecessary punctuation while keeping emoticons and important punctuation
    tweet = tweet.translate(
        str.maketrans(
            "",
            "",
            string.punctuation.replace("!", "").replace("?", "").replace("#", ""),
        )
    )
    # Strip unnecessary whitespace
    return tweet.strip()


def update_sentiment_scores(
    batch: List[Tuple[str, str]], connection_params: dict, local: bool
) -> None:
    """
    Update full_text values for a batch of data in the local SQLite database.

    Args:
        batch: List of (full_text, tweet_id) pairs.
        db_path: The path to the SQLite database file.
    """
    update_query = "UPDATE Tweets SET sentiment_score = ? WHERE tweet_id = ?"
    if not local:
        update_query = update_query.replace("?", "%s")
    with connect_to_database(connection_params, local) as connection:
        execute_queries(connection, [(update_query, batch)])
        connection.commit()


def get_batches(df: pd.DataFrame, batch_size: int = 1000) -> List[pd.DataFrame]:
    """
    Split DataFrame into batches of DataFrames with specified batch size.

    Args:
        df: The DataFrame containing tweet data.
        batch_size: The size of each batch.

    Returns:
        A list of DataFrames, each containing a batch of rows.
    """
    return [df.iloc[i : i + batch_size] for i in range(0, len(df), batch_size)]


def convert_to_list(df: pd.DataFrame) -> List[List]:
    """
    Convert DataFrame with tweet_id as index to a list of lists containing sentiment and tweet_id.

    Args:
        df: The DataFrame with tweet_id as index and sentiment as a column.

    Returns:
        A list of lists containing tweet_id and sentiment.
    """
    tweet_ids = df.index.to_numpy()
    sentiments = df["sentiment"].to_numpy()
    return tuple(zip(sentiments, tweet_ids))
