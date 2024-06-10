# Evaluating Airline Performance using Twitter data

One Paragraph of the project description

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Environment Setup

Python Interpreter Version: 3.10

To be able to create a database in MYSQL using the code, you must set the following environment variables:
DBL_USER, DBL_DATABASE, DBL_PASSWORD, DBL_HOST. The code gets the variables using check_env_vars() function defined in 
_0_Constants\\env_vars.py.

### _0_Constants

This folder contains static pieces of code used throughout the project.

### _1_Tweet_Data_Extraction

Given a folder with jsons containing tweets, our first aim was to clean them.
In order to clean the data, the folder with raw jsons must be put in this directory (_1_Tweet_Data_Extraction),
under the name 'data_raw'. Then one must run the file data_extraction.py.
The result will be one JSON file in this directory, under data_processed//cleaned_tweets_combined.json.

### _2_Insert_Tweets_to_Database

Now that we have the tweets in form of jsons only with the fields that interest us, the next step is to
insert them into an SQL database. We decided to use a MySQL database, it can be created by running the
insert_tweets_to_mysql_db.py file (remember to set up environment variables as stated at the top of this document!!).

Additionally, we decided to use backup in the form of a SQLite database. It can be created by running insert_tweets_to_sqlite_db.py.
After the file successfully executes, the file can be found under Local_Database\local_backup.db.

### _3_Visualizations_Sprint_1

After having uploaded the data to a database, we move on to the first part that can provide us with real insights:
visualizations. To perform them, run EDA_1.ipynb.

Hint: you can specify whether to fetch the data from mysql or sqlite database by modifying the variable
'local' in the get_df_from_db function.

### _4_and_following (to be done)

Next steps here must include, in some form:

1. Extracting the conversations
2. Uploading the conversations to the db (with option to do that both for sqlite and mysql)
3. Uploading the sentiment for tweets to the db (-||-)
4. Uploading the categories for conversations to the db (-||-)
5. Visualizations for Sprint 2
6. Visualizations for Sprint 3?
7. Demo?

## Authors

  - **Kirill Chekmenev**
  - **Jokubas Jasas**
  - **Martynas Kulys**
  - **Joshua Pantekoek**
  - **Igor Banasik**
  - **Nikita Seleznov**
