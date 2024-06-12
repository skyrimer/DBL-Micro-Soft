# SQLite
CREATE_USERS_SQLITE: str = """ 
CREATE TABLE IF NOT EXISTS Users(
    user_id TEXT PRIMARY KEY,
    verified INTEGER NOT NULL,  -- 0 or 1 for boolean
    followers_count INTEGER NOT NULL,
    friends_count INTEGER NOT NULL,
    statuses_count INTEGER NOT NULL,
    creation_time DATETIME NOT NULL,
    default_profile INTEGER NOT NULL,  -- 0 or 1 for boolean
    default_profile_image INTEGER NOT NULL  -- 0 or 1 for boolean
);
"""

CREATE_TWEETS_SQLITE: str = """ 
CREATE TABLE IF NOT EXISTS Tweets(
    tweet_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    full_text TEXT NOT NULL,
    lang TEXT NOT NULL,
    creation_time DATETIME NOT NULL,
    country_code TEXT,
    favorite_count INTEGER NOT NULL,
    retweet_count INTEGER NOT NULL,
    possibly_sensitive INTEGER,  -- 0 or 1 for boolean
    replied_tweet_id TEXT,
    reply_count INTEGER NOT NULL,
    quoted_status_id TEXT,
    quote_count INTEGER NOT NULL,
    sentiment_score REAL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
"""

CREATE_CONVERSATIONS_SQLITE: str = """
CREATE TABLE IF NOT EXISTS Conversations (
    conversation_id INTEGER,
    tweet_order INTEGER,
    tweet_id TEXT,
    PRIMARY KEY (conversation_id, tweet_order),
    FOREIGN KEY (tweet_id) REFERENCES Tweets(tweet_id)
);
"""

CREATE_CONVERSATIONS_CATEGORY_SQLITE: str = """
CREATE TABLE IF NOT EXISTS ConversationsCategory (
    conversation_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL CHECK(category IN (
        'flight delays and cancellations', 
        'booking problems', 
        'check-in troubles', 
        'customer service complaints', 
        'seating and boarding challenges', 
        'in-flight experience', 
        'flight information requests', 
        'refund complaints', 
        'frequent flyer concerns', 
        'safety and security concerns', 
        'special assistance requests', 
        'food and beverage complaints', 
        'overbooking complaints', 
        'technical difficulties', 
        'promotion and offer issues', 
        'lost luggage', 
        'baggage issues',
        'No Category'
    )),
    FOREIGN KEY (conversation_id) REFERENCES Conversations(conversation_id)
);
"""


# MySQL
CREATE_USERS_MYSQL: str = """ 
CREATE TABLE IF NOT EXISTS Users(
    user_id VARCHAR(20) PRIMARY KEY,
    verified TINYINT(1) NOT NULL,
    followers_count INT UNSIGNED NOT NULL,
    friends_count INT UNSIGNED NOT NULL,
    statuses_count INT UNSIGNED NOT NULL,
    creation_time TIMESTAMP NOT NULL,
    default_profile TINYINT(1) NOT NULL,
    default_profile_image TINYINT(1) NOT NULL            
);
"""

CREATE_TWEETS_MYSQL: str = """ 
CREATE TABLE IF NOT EXISTS Tweets(
    tweet_id VARCHAR(20) PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL,
    full_text VARCHAR(1000) NOT NULL,
    lang CHAR(2) NOT NULL,
    creation_time TIMESTAMP NOT NULL,
    country_code CHAR(2),
    favorite_count MEDIUMINT UNSIGNED NOT NULL,
    retweet_count MEDIUMINT UNSIGNED NOT NULL,
    possibly_sensitive TINYINT(1),
    replied_tweet_id VARCHAR(20),
    reply_count MEDIUMINT UNSIGNED NOT NULL,
    quoted_status_id VARCHAR(20),
    quote_count MEDIUMINT UNSIGNED NOT NULL,
    sentiment_score FLOAT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
"""

CREATE_CONVERSATIONS_MYSQL: str = """
CREATE TABLE IF NOT EXISTS Conversations (
    conversation_id MEDIUMINT UNSIGNED,
    tweet_order TINYINT UNSIGNED,
    tweet_id VARCHAR(20),
    PRIMARY KEY (conversation_id, tweet_order),
    FOREIGN KEY (tweet_id) REFERENCES Tweets(tweet_id)
);
"""

CREATE_CONVERSATIONS_CATEGORY_MYSQL: str = """
CREATE TABLE IF NOT EXISTS ConversationsCategory (
    conversation_id MEDIUMINT UNSIGNED PRIMARY KEY,
    category ENUM(
        'flight delays and cancellations', 
        'booking problems', 
        'check-in troubles', 
        'customer service complaints', 
        'seating and boarding challenges', 
        'in-flight experience', 
        'flight information requests', 
        'refund complaints', 
        'frequent flyer concerns', 
        'safety and security concerns', 
        'special assistance requests', 
        'food and beverage complaints', 
        'overbooking complaints', 
        'technical difficulties', 
        'promotion and offer issues', 
        'lost luggage', 
        'baggage issues',
        'No Category'
    ) NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES Conversations(conversation_id)
);
"""
