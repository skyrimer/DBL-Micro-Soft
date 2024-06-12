import os

# Here are paths to all the files used in the project in multiple places.
# If you change a location for any of those files, remember to also change it here!!

# Get a path to the json file with processed tweets
folder_processed_name: str = "data_processed"
local_database_name: str = "local_backup.db"
processed_tweets_json_name: str = "cleaned_tweets_combined.json"

folder_path_processed: str = os.path.dirname(os.getcwd())
folder_processed: str = os.path.join(folder_path_processed, folder_processed_name)
path_processed_tweets_json: str = os.path.join(
    folder_processed, processed_tweets_json_name
)

# Get a path to the local database
path_local_database: str = os.path.join(folder_processed, local_database_name)
path_local_database_notebook: str = os.path.join(
    os.path.dirname(folder_path_processed), folder_processed_name, local_database_name
)
