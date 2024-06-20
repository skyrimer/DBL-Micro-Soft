# Evaluating Airline Performance using Twitter data

This is the code base of Mirco-Soft DBL. This instruction was written by tired and exhausted people, who yet created a comprehensive analysis of Lufthansa Twitter team performance.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes.

## Python version

### Windows

1. **Download Python Installer:**

   - Go to the [official Python download page](https://www.python.org/downloads/).
   - Click on "Windows installer (64-bit)" to download the executable installer.

2. **Run the Installer:**

   - Open the downloaded file to start the installation.
   - Make sure to check the box that says "Add Python 3.12 to PATH".
   - Click on "Customize installation".

3. **Customize Installation:**

   - Ensure all optional features are checked, then click "Next".
   - On the Advanced Options screen, check "Install for all users" and note the installation location.
   - Click "Install" to begin the installation.

4. **Verify Installation:**
   - Open Command Prompt and type:
     ```console
     python --version
     ```
   - You should see `Python 3.12.3`.

### macOS

1. **Download Python Installer:**

   - Go to the [official Python download page](https://www.python.org/downloads/).
   - Click on "macOS 64-bit installer" to download the .pkg file.

2. **Run the Installer:**

   - Open the downloaded .pkg file to start the installation.
   - Follow the prompts to complete the installation.

3. **Verify Installation:**
   - Open Terminal and type:
     ```console
     python3 --version
     ```
   - You should see `Python 3.12.3`.

#### Linux

1. **Add Deadsnakes PPA (For Ubuntu/Debian-based systems):**

   - Open Terminal and add the Deadsnakes PPA:
     ```console
     sudo add-apt-repository ppa:deadsnakes/ppa
     sudo apt update
     ```

2. **Install Python 3.12:**

   - Run the following command to install Python 3.12:
     ```console
     sudo apt install python3.12
     ```

3. **Verify Installation:**
   - Check the installed version by typing:
     ```console
     python3.12 --version
     ```
   - You should see `Python 3.12.3`.

### Verify Installation and Set Up Environment

1. **Create a Virtual Environment:**

   - Navigate to your project directory and run:
     ```console
     python -m venv venv
     ```
   - This creates a virtual environment named `venv`.

2. **Activate the Virtual Environment:**

   - **Windows:**
     ```console
     .\venv\Scripts\activate
     ```
   - **macOS and Linux:**
     ```console
     source venv/bin/activate
     ```

3. **Install Required Packages:**
   - Once the virtual environment is activated, install the required packages for your project:
     ```console
     pip install -r requirements.txt
     ```

### MySQL server setup and Environment variables

Take into account that setting up an online external MySQL server will cost some money. If you do not want to simultaneously work on the database with different instances or pay for the server, we recommend using a local database with Sqlite3 (see '\_2_Insert_Tweets_to_Database' below)

Here are the instructions to set up the MySQL server that is hosted externally using [beget.com][https://beget.com/en]:

- Register at [beget.com][https://cp.beget.com/login] using your full name, email and phone number
- After you fill the Captcha and confirm via SMS, the moderation should be done. Your account will be created after you have received the email from "LTD BEGET" (the email message might be in Russian, but the whole website interface is in English)
- In the email, you have received you will need your login (if in Russian, under name "Логин") and password (if in Russian, under name "Пароль"). Those are going to be `DBL_USER` and `DBL_PASSWORD` environment variables.
- After that login in using login and password from the email, and go to [MySQL][https://cp.beget.com/mysql]
- At the "Add database" section, fill in the fields for "Database name" and "Password". "Database name" is both the `DBL_USER` and `DBL_DATABASE` environment variables value, while "Password" will be `DBL_PASSWORD` environment variable.
- After you filled out the fields, click "Add new" and wait until your database appears at the end of the page
- Click on green plus emoji to add access to DB. Set "Single access for different IP addresses" to true (tick the box) and then set the same password in "Password" field. Then click "add new"
- After that anyone with the username, database name, password and host name (if the website is not deprecated your `DBL_HOST` should be `{your username from username}.beget.tech`. It can also be found on the left side bar next to "Server")

If this website is deprecated or does not work, here are some resources on how to set up an external MySQL server online:

- https://aws.amazon.com/free/database/
- https://www.amazonaws.cn/en/getting-started/tutorials/create-mysql-db/

To be able to create a remote MySQL database using the code, you must set the following environment variables:

- `DBL_USER` - username
- `DBL_DATABASE` - name of the database,
- `DBL_PASSWORD` - password to the database,
- `DBL_HOST` - host name.

For [beget.com][https://cp.beget.com/login] all of the values were discussed in previous section.
The code gets the variables using `check_env_vars()` function defined in `_0_Constants\\env_vars.py`. Thus, if security concerns is not and issue, `check_env_vars()` can be modified to explicitly return the values.

If you are not planning to use MySQL and will be working with local SQLite3 database then you don't need to set the environment variables.

## How to run

1. Unzip the DBL-Micro-Soft-1.zip and open the folder in your code editor or command prompt.

2. Navigate to the project directory:

```console
cd Final_code
```

3. Create a virtual environment (optional but recommended):

```console
python -m venv venv
```

4. Activate the virtual environment (if you have created it in the previous step):
   `.\venv\Scripts\activate` - for Windows
   `source venv/bin/activate` - for Mac

5. Install the required dependencies:

```console
pip install -r requirements.txt
```

6. Run any of the required scripts using

```console
python folder/python_module.py
```

, where you should change `folder/python_module.py` to the path to the module that you want to run.

### \_0_Constants

This folder contains constants and utility functions used throughout the project. All the functions were tested before, but you need to modify anything like the database utilities or predefined paths, then all the functions and constants can be found in modules in this folder. All of the functions have docstring documentation, so it should be clear what are the doing and how to use them.

### \_1_Tweet_Data_Extraction

Given a folder with JSONs containing tweets, our first aim was to clean them.
In order to clean the data, the folder with raw JSONs must be put in the main directory of the project (next to folders `Split N`, `Final_code` and etc), under the name `data_raw`. Then one must run the file `data_extraction.py`.
The result will be one JSON file in this directory, under `data_processed/cleaned_tweets_combined.json`.

### \_2_Insert_Tweets_to_Database

Now that we have the tweets in form of JSON only with the fields that interest us, the next step is to insert them into an SQL database. We decided to use a MySQL database (and Sqlite3 as the backup database in case something happens to the server), it can be created by running the
insert_to_db.py file (remember to set up environment variables as stated at the top of this document!!). Before executing the script, you must check 3 parameters:

- `local` - whether the Sqlite or MySQL should be filled with data (set to True if you want to use the local version Sqlite3, and False if you want to use external server MYSQL)
- `reset` - whether you want to fully reset the database before insertion (Set to True if you want to reset the database, and False if not)
- `batch_size` - how many rows of data will be uploaded at the same time. Bigger batches increase the running time, but require more memory.

After the file successfully executes, MySQL database will be updated with `Tweets` and `Users` information (If `local` was set to `True`, then the database can be found under `data_processed\local_backup.db`).

### \_3_Visualizations_Sprint_1

After having uploaded the data to a database, we move on to the first part that can provide us with real insights through simple visualizations. To perform them, run `EDA_1.ipynb`. In order to switch between the local and server version of the database, change variable `local` in the first cell of "Loading" section.

### \_4_Conversations

This folder features the conversation extraction algorithm as well as its upload to the database. In order to identify all the conversations and upload them to database under `Conversations` table, you need to run `conversation_extraction.ipynb`.
As usual, `local` variable in the first cell of "Local" section switches between the local and server versions of the database. `batch_size` in the last cell defines how many rows of data will be uploaded at the same time.

### \_5_Sentiment_Score

This folder features the sentiment scores utilities and upload of tweets sentiment scores to the database.

- `sentiment_scores.ipynb` is the file that gets and uploads the sentiment scores to the database. `local` and `batch_size` variables have the same meaning as in files before.
- `sentiment_accuracy.ipynb` is the file that contains evaluation of the deep learning model accuracy. The way it is done, is by comparing the labels to the pre labelled dataset that found [here][https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment].

#### Notes on running the sentiment scores

This installation guide explains how to get the python version that we were working with, which is python `3.12.3`. However, for the semantic analysis part in order to significantly increase the runtime performance for such heavy operation, we used an external website [Kaggle][https://www.kaggle.com], which has the necessary version of python (<3.11) and GPU drivers with necessary drivers in order to use GPU acceleration. Thus, the following guide will still work, yet getting sentiment scores will take a while (roughly 93 hours depending on machine specs to get all sentiment scores).
If you planning to use GPU acceleration when getting sentiment scores for tweets, then you need to do the following:

1. Create an account on [Kaggle][https://www.kaggle.com]
2. Verify the account using the phone number
3. Create a new notebook and import the `sentiment_scores.ipynb` module as well as the functions and constants used in it (namely `clean_mentions, get_batches, apply_sentiment_analysis, convert_to_list, update_sentiment_scores` from `sentiment_utils.py` and `get_dataframe_from_query, form_connection_params` from `_0_Constants\database_utils.py`)
   4 Adjust the behaviour of `form_connection_params`:
   4.1. If you're planning to use MySQL server, then explicitly state the connection parameters or use environment variables ([guide how to use environment variables on Kaggle][https://www.kaggle.com/code/jamesmcguigan/kaggle-environment-variables-os-environ])
   4.2. If you're planning to use SQLite, then you need to upload your local database as the dataset, copy the database into working directory using `!cp "/kaggle/input/{database_path}" kaggle/working/`, and then adjust the paths in the paths accordingly.
4. Change the session options to use GPU accelerator (, and persistence to "Files only" if you're using the local version)
5. Run the script either manually or click "Save version" and let it run on the server (it runs for 12 hours or until it is done). If you're using the local version, then you can download the updated database from the working folder.

An example code could be found under `kaggle_local.ipynb`

### \_6_Categorisation

This folder contains retrieving topics of the conversations and conversations that should have been started, which should be ran in the following order:

- `category_train.ipynb` - trains the SVM model on the dataset. The one that we've collected is under `clean_labels.xlsx` but you can you which ever one you like.
- `category_upload.ipynb` - extracts all the categories and uploads it to the database. `local` and `batch_size` variables have the same meaning as in files before.
- `NonResponses.ipynb` - extracts all the non-responses by Lufthansa and saves them into folders for Performance Evaluation and the Demo.

### \_7_Visualizations_Sprint_2

This folder contains all the visualisations that were used to get intermediate results of sentiment analysis and business idea. Some of the graphs were just used to provide additional insights and are not directly related to anything. To perform them, run `EDA_2.ipynb`. In order to switch between the local and server version of the database, change variable `local` in the first cell of "Loading" section.

### \_8_PerformanceEvaluation

This folder contains all the final visualisations that were considered for the poster. A big part of it was just exploration of what we have collected, thus a lot of graphs might be not as neat as they should be for the presentation. To perform them, run `summarisation.ipynb`. In order to switch between the local and server version of the database, change variable `local` in the first cell of "Loading" section.

### \_9_PerformanceEvaluation

This folder contains the demo code that generates the graphs and statistics for the poster. To perform them, run `demo.ipynb`. In order to switch between the local and server version of the database, change variable `local` in the first cell of "Loading" section. If you want to adjust the time spans then change `start_time` and `end_time` in the format of `yyyy-mm-dd`.

## Authors

- **Kirill Chekmenev**
- **Jokubas Jasas**
- **Martynas Kulys**
- **Joshua Pantekoek**
- **Igor Banasik**
- **Nikita Seleznov**
