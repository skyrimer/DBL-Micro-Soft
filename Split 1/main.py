from data_extraction import start_extraction
from general_data_extraction import start_general_extraction


def main():
    general_extraction: bool = True  # True = don't separate companies into files, False = each company independently
    if general_extraction:
        sample_data_only: bool = True  # General extraction: True = only the (5) sample JSON files, False = all data
        start_general_extraction(sample_data_only)
    else:
        start_extraction()


if __name__ == "__main__":
    main()
