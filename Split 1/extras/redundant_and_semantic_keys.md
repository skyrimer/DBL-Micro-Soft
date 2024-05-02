## Redundant Keys (data_processing.py)(some are missing, will be updated later, refer to kept keys for now):
### Should use str format of the following keys: 
- **'id'**
- **'in_reply_to_status_id'**
- **'in_reply_to_user_id'**
- **'user.id'** 
- **'quoted_status_id'**

### Keys with no real significance:
- **'truncated'** (equivalent to `if 'extended_tweet' in tweet.keys()`)
- **'in_reply_to_screen_name'** (conversations should be matched based on `user.id_str`)
- **'user.url'**
- **'user.description'**
- **'user.utc_offset'**
- **'user.time_zone'**
- **'user.geo_enabled'**
- **'user.lang'** (for translation purposes, refer to `lang` key instead)
- **'user.contributors_enabled'**
- **'user.is_translator'**
- **'user.profile_background_color'**
- **'user.profile_background_image_url'**
- **'user.profile_background_image_url_https'**
- **'user.profile_background_tile'**
- **'user.profile_link_color'**
- **'user.profile_sidebar_border_color'**
- **'user.profile_sidebar_fill_color'**
- **'user.profile_text_color'**
- **'user.profile_use_background_image'**
- **'user.profile_image_url'**
- **'user.profile_image_url_https'**
- **'user.profile_banner_url'**
- **'user.follow_request_sent'**
- **'user.notifications'**
- **'user.translator_type'**
- **'user.protected'**
- **'user.listed_count'** (there are better keys for bot-verification)
- **'user.favourites_count'** (there are better keys for bot-verification)
- **'user.following'** (there are better keys for bot-verification)
- **'extended_tweet.display_text_range'**
- **'extended_tweet.entities.hashtags'**
- **'extended_tweet.entities.urls'**
- **'extended_tweet.entities.symbols'**
- **'entities.hashtags'**
- **'entities.urls'**
- **'entities.symbols'**
- **'favorited'** (authenticated user data, irrelevant)
- **'retweeted'** (authenticated user data, irrelevant)
- **'filter_level'**
- **'matching_rules'**
- **'geo'** (deprecated key, use `coordinates` instead)
- **'contributors'**
- **'timestamp_ms'**

## Sentiment Analysis Keys
### All kept keys within the objects (database fields):
- **'id_str'**
- **'text'**
- **'source'**
- **'in_reply_to_status_id_str'**
- **'user'**
  - **'id_str'**
  - **'location'**
  - **'verified'**
  - **'followers_count'**
  - **'friends_count'**
  - **'statuses_count'**
  - **'created_at'**
  - **'default_profile'**
  - **'default_profile_image'**
- **'place'**
  - **'country_code'**
  - **some extras**
- **'quote_count'**
- **'reply_count'**
- **'retweet_count'**
- **'favorite_count'**
- **'lang'**
- **'extended_tweet'**
  - **'full_text'**
- **'timestamp_ms'**
- **'possibly_sensitive'**

### Keys used for sentiment analysis:
- **'text'** if `extended_tweet.full_text` does not exist
- **'extended_tweet'.'full_text'** 


### All the keys are only preliminary and this information is subject to change
