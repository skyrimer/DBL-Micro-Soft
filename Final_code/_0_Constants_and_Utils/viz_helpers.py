from typing import Union

import numpy as np
import pycountry

# This is a file with helper functions used for visualizations


def get_country_name(country_code: str, default: str = "Unknown Country") -> str:
    """
    Convert a two-letter country code (ISO 3166-1 alpha-2) to its full country name.

    Parameters:
    country_code (str): The two-letter ISO 3166-1 alpha-2 country code.

    Returns:
    str: The full name of the country or a message indicating the code was not found.
    """
    try:
        country = pycountry.countries.get(alpha_2=country_code, default=default)
    except LookupError:
        return default
    if country != default:
        country = country.name
    return country


def get_full_language_name(
    language_code: str, default: str = "Undefined Language"
) -> str:
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


def get_size_of(size_bytes: Union[float, int]) -> str:
    """
    Convert a size in bytes to a human-readable string with appropriate units.

    Parameters:
    size_bytes (Union[float, int]): The size in bytes.

    Returns:
    str: A human-readable string representing the size in appropriate units.
    """
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
