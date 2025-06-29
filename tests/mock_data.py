"""
Mock data for unit tests including sample tweets in UK and US English
"""

# Sample tweets in UK English
UK_ENGLISH_TWEETS = [
    {
        "created_at": "Wed Oct 11 10:30:00 +0000 2023",
        "full_text": "The colour of autumn leaves is absolutely brilliant this year. Centre of town looks lovely.",
        "text": "The colour of autumn leaves is absolutely brilliant this year. Centre of town looks lovely.",
        "coordinates": None,
        "place": {"country": "United Kingdom", "name": "London"},
        "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
        "id": 1712345678901234567
    },
    {
        "created_at": "Thu Oct 12 14:15:00 +0000 2023",
        "full_text": "Favour doing this properly rather than rushing through it. Organisation is key to success.",
        "text": "Favour doing this properly rather than rushing through it. Organisation is key to success.",
        "coordinates": None,
        "place": {"country": "United Kingdom", "name": "Manchester"},
        "source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
        "id": 1712345678901234568
    }
]

# Sample tweets in US English
US_ENGLISH_TWEETS = [
    {
        "created_at": "Wed Oct 11 10:30:00 +0000 2023",
        "full_text": "The color of fall leaves is absolutely amazing this year. Downtown looks beautiful.",
        "text": "The color of fall leaves is absolutely amazing this year. Downtown looks beautiful.",
        "coordinates": None,
        "place": {"country": "United States", "name": "New York"},
        "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
        "id": 1712345678901234569
    },
    {
        "created_at": "Thu Oct 12 14:15:00 +0000 2023",
        "full_text": "Favor doing this right instead of rushing through it. Organization is key to success.",
        "text": "Favor doing this right instead of rushing through it. Organization is key to success.",
        "coordinates": None,
        "place": {"country": "United States", "name": "Los Angeles"},
        "source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
        "id": 1712345678901234570
    }
]

# Combined sample tweets for mixed testing
MIXED_TWEETS = UK_ENGLISH_TWEETS + US_ENGLISH_TWEETS

# Sample configuration data
SAMPLE_CONFIG = {
    "config": {
        "access_token": "test_access_token",
        "access_secret": "test_access_secret", 
        "consumer_key": "test_consumer_key",
        "consumer_secret": "test_consumer_secret",
        "target": "test_user",
        "search_terms": ["test", "example", "sample"],
        "dialect": "en-US"
    }
}

# Sample processed tweet data (output of TweetTextExtractor)
SAMPLE_PROCESSED_TWEETS = [
    {
        "date": "Wed Oct 11 10:30:00 +0000 2023",
        "text": "The color of fall leaves is absolutely amazing this year. Downtown looks beautiful.",
        "coordinates": None,
        "place": {"country": "United States", "name": "New York"},
        "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
        "created_at": "Wed Oct 11 10:30:00 +0000 2023"
    },
    {
        "date": "Thu Oct 12 14:15:00 +0000 2023", 
        "text": "Favor doing this right instead of rushing through it. Organization is key to success.",
        "coordinates": None,
        "place": {"country": "United States", "name": "Los Angeles"},
        "source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
        "created_at": "Thu Oct 12 14:15:00 +0000 2023"
    }
]