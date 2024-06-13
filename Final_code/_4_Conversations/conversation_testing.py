import pandas as pd
from conversation_algorithm import extract_conversations

test_cases = [
    {
        "name": "1. Simple Conversation Between User and Airline",
        "data": {
            "tweet_id": ["1", "2", "3", "4"],
            "user_id": ["airline", "user_a", "airline", "user_a"],
            "replied_tweet_id": [None, "1", "2", "3"],
            "tweet_creation_time": [
                "2023-05-01T10:00:00Z",
                "2023-05-01T10:05:00Z",
                "2023-05-01T10:10:00Z",
                "2023-05-01T10:15:00Z",
            ],
        },
        "expected": [["1", "2", "3", "4"]],
    },
    {
        "name": "2. User-Initiated Conversation",
        "data": {
            "tweet_id": ["1", "2", "3"],
            "user_id": ["user_a", "airline", "user_a"],
            "replied_tweet_id": [None, "1", "2"],
            "tweet_creation_time": [
                "2023-05-01T11:00:00Z",
                "2023-05-01T11:05:00Z",
                "2023-05-01T11:10:00Z",
            ],
        },
        "expected": [["1", "2", "3"]],
    },
    {
        "name": "3. More Than Two Users Involved",
        "data": {
            "tweet_id": ["1", "2", "3", "4"],
            "user_id": ["user_a", "airline", "user_b", "airline"],
            "replied_tweet_id": [None, "1", "2", "3"],
            "tweet_creation_time": [
                "2023-05-01T12:00:00Z",
                "2023-05-01T12:05:00Z",
                "2023-05-01T12:10:00Z",
                "2023-05-01T12:15:00Z",
            ],
        },
        "expected": [["1", "2"], ["2", "3", "4"]],
    },
    {
        "name": "4. Conversation Branches Out",
        "data": {
            "tweet_id": ["1", "2", "3", "4", "5"],
            "user_id": ["airline", "user_a", "airline", "user_a", "user_b"],
            "replied_tweet_id": [None, "1", "2", "3", "2"],
            "tweet_creation_time": [
                "2023-05-01T13:00:00Z",
                "2023-05-01T13:05:00Z",
                "2023-05-01T13:10:00Z",
                "2023-05-01T13:15:00Z",
                "2023-05-01T13:20:00Z",
            ],
        },
        "expected": [["2", "5"], ["1", "2", "3", "4"]],
    },
    {
        "name": "5. Non-Reply Initial Tweet by Airline",
        "data": {
            "tweet_id": ["1", "2"],
            "user_id": ["airline", "user_a"],
            "replied_tweet_id": [None, "1"],
            "tweet_creation_time": ["2023-05-01T14:00:00Z", "2023-05-01T14:05:00Z"],
        },
        "expected": [["1", "2"]],
    },
    {
        "name": "6. Non-Reply Initial Tweet by User",
        "data": {
            "tweet_id": ["1", "2"],
            "user_id": ["user_a", "airline"],
            "replied_tweet_id": [None, "1"],
            "tweet_creation_time": ["2023-05-01T15:00:00Z", "2023-05-01T15:05:00Z"],
        },
        "expected": [["1", "2"]],
    },
    {
        "name": "8. Same User Replies to Themselves",
        "data": {
            "tweet_id": ["1", "2", "3"],
            "user_id": ["user_a", "user_a", "user_a"],
            "replied_tweet_id": [None, "1", "2"],
            "tweet_creation_time": [
                "2023-05-01T17:00:00Z",
                "2023-05-01T17:05:00Z",
                "2023-05-01T17:10:00Z",
            ],
        },
        "expected": [],
    },
    {
        "name": "9. Mixed Order of Tweets",
        "data": {
            "tweet_id": ["3", "1", "2"],
            "user_id": ["user_a", "airline", "user_a"],
            "replied_tweet_id": [None, "3", "1"],
            "tweet_creation_time": [
                "2023-05-01T18:00:00Z",
                "2023-05-01T18:05:00Z",
                "2023-05-01T18:10:00Z",
            ],
        },
        "expected": [["3", "1", "2"]],
    },
    {
        "name": "10. Multiple Independent Conversations",
        "data": {
            "tweet_id": ["1", "2", "3", "4", "5", "6"],
            "user_id": ["airline", "user_a", "airline", "user_b", "airline", "user_a"],
            "replied_tweet_id": [None, "1", None, "3", None, "5"],
            "tweet_creation_time": [
                "2023-05-01T19:00:00Z",
                "2023-05-01T19:05:00Z",
                "2023-05-01T19:10:00Z",
                "2023-05-01T19:15:00Z",
                "2023-05-01T19:20:00Z",
                "2023-05-01T19:25:00Z",
            ],
        },
        "expected": [["1", "2"], ["3", "4"], ["5", "6"]],
    },
    {
        "name": "11. Nested Replies",
        "data": {
            "tweet_id": ["1", "2", "3", "4"],
            "user_id": ["airline", "user_a", "airline", "user_a"],
            "replied_tweet_id": [None, "1", "2", "3"],
            "tweet_creation_time": [
                "2023-05-01T20:00:00Z",
                "2023-05-01T20:05:00Z",
                "2023-05-01T20:10:00Z",
                "2023-05-01T20:15:00Z",
            ],
        },
        "expected": [["1", "2", "3", "4"]],
    },
]


for test_case in test_cases:
    df = pd.DataFrame(test_case["data"]).set_index("tweet_id")
    df["tweet_creation_time"] = pd.to_datetime(df["tweet_creation_time"])
    df = df.sort_values("tweet_creation_time", ascending=False)
    result = extract_conversations(df, test_case["data"]["user_id"])
    assert sorted(result) == sorted(
        test_case["expected"]
    ), f"'{test_case['name']}' failed: expected {test_case['expected']}, got {result}"
    print(f"'{test_case['name']}' passed.")
    print()
print("All tests passed!")
