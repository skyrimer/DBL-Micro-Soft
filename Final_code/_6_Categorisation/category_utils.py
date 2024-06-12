import re
from typing import List

import pandas as pd


def clean_mentions(text):
    mention_pattern = r"@([A-Za-z0-9_]+)"
    url_pattern = r"https?://\S+|www\.\S+"
    rt_pattern = r"^RT\s+"

    text = re.sub(mention_pattern, "", text)
    text = re.sub(url_pattern, "", text)
    text = re.sub(rt_pattern, "", text)

    return text.strip()


def get_batches(df: pd.DataFrame, batch_size: int = 1000) -> List[pd.DataFrame]:
    return [df.iloc[i : i + batch_size] for i in range(0, len(df), batch_size)]


def convert_to_list(df: pd.DataFrame) -> List[List]:
    # Ensure the index contains the conversation IDs as native Python int
    conversation_ids = df.index.to_list()  # Convert to list of native Python int
    # Convert categories to strings
    categories = df["category"].astype(str).to_list()  # Convert to list of str
    # Combine the conversation IDs and categories into a list of tuples
    return list(zip(categories, conversation_ids))
