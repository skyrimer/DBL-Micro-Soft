## Redundant Keys (data_processing.py):

### (_str format should be used, mainly because of the official Twitter documentation, also bigint issue in db):

- **'id'**
- **'in_reply_to_status_id'**
- **'user.id'**
- **'quoted_status_id'**

### Keys removed for other reasons

- **'created_at'** (will be using timestamp_ms for easier analysis, mainly the
  time taken to respond)
- **'truncated'** (equivalent to `if 'extended_tweet' in tweet.keys()`)
- **'display_text_range'** (tweet's length is not very useful, also we can
  alternatively find the length from the tweet's text)
- **'in_reply_to_user_id'** (can be found by looking at the parent tweet, also
  provides no real use)
- **'in_reply_to_user_id_str'** (can be found by looking at the parent tweet,
  also provides no real use)
- **'in_reply_to_screen_name'** (can be found by looking at the parent tweet,
  also provides no real use)
- **'user.name'** (users should be identified by id's, also name can be easily
  changed)
- **'user.screen_name'** (users should be identified by id's, not handles)
- **'user.url'** (won't be using profile urls in the analysis)
- **'user.description'** (should refer to the tweet content rather than user's
  description when doing sentiment analysis)
- **'user.utc_offset'** (won't be using in the analysis, also a deprecated
  attribute)
- **'user.time_zone'** (won't be using in the analysis, also a deprecated
  attribute)
- **'user.geo_enabled'** (won't be using in the analysis, also a deprecated
  attribute)
- **'user.lang'** (won't be using in the analysis, also a deprecated attribute)
- **'user.contributors_enabled'** (won't be using in the analysis, also a
  deprecated attribute)
- **'user.is_translator'** (won't be using in the analysis, also a deprecated
  attribute)
- **'user.profile_background_color'** (we will use follow count, and profile's
  age / default-account state as indicators for bot accounts)
- **'user.profile_background_image_url'** (we will use follow count, and
  profile's age / default-account state as indicators for bot accounts)
- **'user.profile_background_image_url_https'** (we will use follow count, and
  profile's age / default-account state as indicators for bot accounts)
- **'user.profile_background_tile'** (we will use follow count, and profile's
  age / default-account state as indicators for bot accounts)
- **'user.profile_link_color'** (we will use follow count, and profile's age /
  default-account state as indicators for bot accounts)
- **'user.profile_sidebar_border_color'** (we will use follow count, and
  profile's age / default-account state as indicators for bot accounts)
- **'user.profile_sidebar_fill_color'** (we will use follow count, and profile's
  age / default-account state as indicators for bot accounts)
- **'user.profile_text_color'** (we will use follow count, and profile's age /
  default-account state as indicators for bot accounts)
- **'user.profile_use_background_image'** (we will use follow count, and
  profile's age / default-account state as indicators for bot accounts)
- **'user.profile_image_url'** (we will use follow count, and profile's age /
  default-account state as indicators for bot accounts)
- **'user.profile_image_url_https'** (we will use follow count, and profile's
  age / default-account state as indicators for bot accounts)
- **'user.profile_banner_url'** (we will use follow count, and profile's age /
  default-account state as indicators for bot accounts)
- **'user.follow_request_sent'** (authorised accounts only, also a deprecated
  attribute)
- **'user.notifications'** (authorised accounts only, also a deprecated
  attribute)
- **'user.translator_type'** (not used in analysis, also a deprecated attribute)
- **'user.protected'** (private account indicator, not an indicator of a bot
  account, will be using user.verified insteaad)
- **'user.listed_count'** (how many lists the user is a part of, there are
  better metrics for bot identification)
- **'user.favourites_count'** (how many tweets the user has favourited, doesn't
  help identify bots - scripts can be set to favourite all/none tweets in the
  feed)
- **'user.following'** (authorised users only, also a deprecated attribute)
- **'entities'** (hashtags, mentions, etc., all of which can be found in `text`)
- **'extended_tweet.display_text_range'** (see `diplay_text_range`)
- **'extended_tweet.entities'** (see `entities`)
- **'extended_tweet.extended_entities'** (see `entities`)
- **'quoted_status_id'** (TODO: ADD REASON)
- **'quoted_status'** (TODO: ADD REASON)
- **'favorited'** (authorised users only, not needed for analysis)
- **'coordinates'** (outside the scope of our abilities to analyze)
- **'place.attributes'** (we will use only place.country_code for geo analysis)
- **'place.bounding_box'** (we will use only place.country_code for geo analysis)
- **'place.country'** (we will use only place.country_code for geo analysis)
- **'place.full_name'** (we will use only place.country_code for geo analysis)
- **'place.id'** (we will use only place.country_code for geo analysis)
- **'place.name'** (we will use only place.country_code for geo analysis)
- **'place.place_type'** (we will use only place.country_code for geo analysis)
- **'place.url'** (we will use only place.country_code for geo analysis)
- **'retweeted'** (authorised users only, won't be used in the analysis)
- **'filter_level'** (related to receiving data via API, irrelevant for our 
  analysis)
- **'matching_rules'** (related to receiving data via API, irrelevant for our 
  analysis)
- **'geo'** (deprecated, also we will use place.country_code for geo analysis)
- **'contributors'** (deprecated, unclear purpose, won't be used)
- **'is_quote_status'** (can be checked via the value of `quoted_status`)
- **'retweeted_status'** 
- **'quoted_status_permalink'** (no documentation about it, also won't be 
  needing links in analysis)
- **'extended_entities'** (see `entities`)

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
