import os

# Here are paths to all the files used in the project in multiple places.
# If you change a location for any of those files, remember to also change it here!!

# Get a path to the json file with processed tweets
path_processed_tweets_json = os.path.join((
        os.path.dirname(
            os.getcwd()
            )
        ),
    "_1_Tweet_Data_Extraction", "data_processed", "cleaned_tweets_combined.json")

# Get a path to the local database
path_local_database = os.path.join((
        os.path.dirname(
            os.getcwd()
            )
        ),
    "Local_Database", "local_backup.db")

print(path_local_database)