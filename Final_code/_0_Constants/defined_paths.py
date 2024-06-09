import os

# Get a path to the json file with processed tweets
path_processed_tweets_json = os.path.join((
        os.path.dirname(
            os.getcwd()
            )
        ),
    "_1_Tweet_Data_Extraction", "data_processed", "cleaned_tweets_combined.json")

# Get a path to the local database
