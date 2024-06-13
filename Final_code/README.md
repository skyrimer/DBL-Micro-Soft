# Evaluating Airline Performance using Twitter data

One Paragraph of the project description

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Environment Setup
## Python version
Note: this installation guide explains how to get the python version that we were working with, which is python 3.12.3. However, for the semantic analysis part in order to significantly increase the runtime performance for such heavy operation, we used an external website [Kaggle][https://www.kaggle.com], which has the necessary version of python (<3.11) and GPU drivers in order to use GPU acceleration. Thus, the following guide will still work, yet if you are not planning to use GPU acceleration when getting sentiment scores for tweets.
### Windows

1. **Download Python Installer:**
   - Go to the [official Python download page](https://www.python.org/downloads/release/python-3125/).
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

## macOS

1. **Download Python Installer:**
   - Go to the [official Python download page](https://www.python.org/downloads/release/python-3125/).
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

### Linux

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

### Environment variables

To be able to create a remote MySQL database using the code, you must set the following environment variables:
- `DBL_USER` - username
- `DBL_DATABASE` - name of the database,
- `DBL_PASSWORD` - password to the database,
- `DBL_HOST` - host name.

The code gets the variables using `check_env_vars()` function defined in `_0_Constants\\env_vars.py`. Thus, if security concerns is not and issue, check_env_vars() can be modified to explicitly return the values.

## How to run 
1. Clone the repository:
```console
git clone https://github.com/skyrimer/DBL-Micro-Soft.git
```

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
### _0_Constants

This folder contains constants and utility functions used throughout the project.

### _1_Tweet_Data_Extraction

Given a folder with JSONs containing tweets, our first aim was to clean them.
In order to clean the data, the folder with raw JSONs must be put in the main directory of the project (next to folders `Split N`, `Final_code` and etc), under the name 'data_raw'. Then one must run the file data_extraction.py.
The result will be one JSON file in this directory, under `data_processed/cleaned_tweets_combined.json`.

### _2_Insert_Tweets_to_Database

Now that we have the tweets in form of JSON only with the fields that interest us, the next step is to insert them into an SQL database. We decided to use a MySQL database (and Sqlite3 as the backup database in case something happens to the server), it can be created by running the
insert_to_db.py file (remember to set up environment variables as stated at the top of this document!!). Before executing the script, you must check 3 parameters:
- `local` - whether the Sqlite or MySQL should be filled with data
- `reset` -  whether you want to fully reset the database before insertion
- `batch_size` - how many rows of data will be uploaded at the same time. Bigger batches increase the running time, but require more memory.

After the file successfully executes, the file can be found under `data_processed\local_backup.db`.

### _3_Visualizations_Sprint_1

After having uploaded the data to a database, we move on to the first part that can provide us with real insights through simple visualizations. To perform them, run EDA_1.ipynb. In order to switch between the local and server version of the database, change variable `local` in the first cell of "Loading" section.

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
