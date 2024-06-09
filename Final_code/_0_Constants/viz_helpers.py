import pycountry
import pandas as pd
import numpy as np

# This is a file with helper functions used for visualizations

def get_country_name(country_code: str, default: str = "Unknown Country") -> str:
    """
    Convert a two-letter country code (ISO 3166-1 alpha-2|) to its full country name.

    Parameters:
    country_code (str): The two-letter ISO 3166-1 alpha-2 country code.

    Returns:
    str: The full name of the country or a message indicating the code was not found.
    """
    country = pycountry.countries.get(alpha_2=country_code, default=default)
    if country != default:
        country = country.name
    return country


def get_full_language_name(language_code: str,
                           default: str = "Undefined Language") -> str:
    """
    Convert a two-letter language code (ISO 639-1) to its full language name.

    Parameters:
    language_code (str): The two-letter ISO 639-1 language code.

    Returns:
    str: The full name of the language or a message indicating the code was not found.
    """
    if language_code == "Other languages":
        return language_code
    language = pycountry.languages.get(alpha_2=language_code, default=default)
    if language != default:
        language = language.name
    return language

def identify_dtype(column: pd.Series) -> str:
    """
    Identifies the most suitable data type for a pandas Series without loss of information.

    Args:
    column (pd.Series): The pandas Series for which the data type needs to be identified.

    Returns:
    str: Suggested data type as a string.
    """
    # Check if the column can be converted to numeric types (int or float)
    if pd.api.types.is_numeric_dtype(column):
        if not pd.to_numeric(column.dropna(), errors='coerce').notna().all():
            return 'object'  # Fallback if numeric conversion fails

        if not (column.dropna() % 1 == 0).all():
            return 'float'
        # Check range to decide between int types
        min_val, max_val = column.min(), column.max()
        if np.iinfo(np.int8).min <= min_val <= np.iinfo(np.int8).max and max_val <= np.iinfo(np.int8).max:
            return 'int8'
        elif np.iinfo(np.int16).min <= min_val <= np.iinfo(np.int16).max and max_val <= np.iinfo(np.int16).max:
            return 'int16'
        elif np.iinfo(np.int32).min <= min_val <= np.iinfo(np.int32).max and max_val <= np.iinfo(np.int32).max:
            return 'int32'
        else:
            return 'int64'
    # Check if the column can be converted to datetime
    with contextlib.suppress(ValueError, TypeError):
        pd.to_datetime(column)
        return 'datetime'
    # Check if the column should be categorical
    if pd.api.types.is_object_dtype(column):
        num_unique_values = len(column.unique())
        num_total_values = len(column)
        if num_unique_values / num_total_values < 0.5:
            return 'category'

    # Default to object type if none of the above conditions are met
    return 'object'

def get_size_of(size_bytes: float | int) -> str:
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    # Using numpy to calculate the logarithm base 1024
    i = int(np.floor(np.log(size_bytes) / np.log(1024)))
    # Using numpy to calculate power of 1024
    p = np.power(1024, i)
    # Computing the size division
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def blob_to_datetime(blob: str) -> pd.Timestamp:
    return pd.to_datetime(blob)