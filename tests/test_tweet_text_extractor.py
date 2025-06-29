"""
Unit tests for TweetTextExtractor class
"""
import unittest
from twitter_shill_hunter.tweet_text_extractor import TweetTextExtractor
from mock_data import UK_ENGLISH_TWEETS, US_ENGLISH_TWEETS, MIXED_TWEETS


class TestTweetTextExtractor(unittest.TestCase):
    """Test cases for TweetTextExtractor"""

    def setUp(self):
        """Set up test fixtures"""
        self.uk_tweets = UK_ENGLISH_TWEETS
        self.us_tweets = US_ENGLISH_TWEETS
        self.mixed_tweets = MIXED_TWEETS
        # Clear the class variable before each test
        TweetTextExtractor.processed_tweets = []

    def test_extract_text_with_uk_tweets(self):
        """Test extraction of UK English tweets"""
        extractor = TweetTextExtractor(self.uk_tweets)
        result = extractor.extract_text()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['text'], 
                        "The colour of autumn leaves is absolutely brilliant this year. Centre of town looks lovely.")
        self.assertEqual(result[0]['date'], "Wed Oct 11 10:30:00 +0000 2023")
        self.assertEqual(result[0]['place']['name'], "London")

    def test_extract_text_with_us_tweets(self):
        """Test extraction of US English tweets"""
        extractor = TweetTextExtractor(self.us_tweets)
        result = extractor.extract_text()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['text'],
                        "The color of fall leaves is absolutely amazing this year. Downtown looks beautiful.")
        self.assertEqual(result[0]['date'], "Wed Oct 11 10:30:00 +0000 2023")
        self.assertEqual(result[0]['place']['name'], "New York")

    def test_extract_text_with_mixed_tweets(self):
        """Test extraction of mixed UK/US English tweets"""
        extractor = TweetTextExtractor(self.mixed_tweets)
        result = extractor.extract_text()
        
        self.assertEqual(len(result), 4)
        # Check UK tweet
        self.assertIn("colour", result[0]['text'])
        # Check US tweet  
        self.assertIn("color", result[2]['text'])

    def test_extract_text_with_full_text_field(self):
        """Test extraction handles both 'text' and 'full_text' fields"""
        tweet_with_full_text = [{
            "created_at": "Wed Oct 11 10:30:00 +0000 2023",
            "full_text": "This is the full text field",
            "coordinates": None,
            "place": None,
            "source": "test"
        }]
        
        extractor = TweetTextExtractor(tweet_with_full_text)
        result = extractor.extract_text()
        
        self.assertEqual(result[0]['text'], "This is the full text field")

    def test_extract_text_with_text_field_only(self):
        """Test extraction falls back to 'text' field when 'full_text' not available"""
        tweet_with_text_only = [{
            "created_at": "Wed Oct 11 10:30:00 +0000 2023",
            "text": "This is the text field",
            "coordinates": None,
            "place": None,
            "source": "test"
        }]
        
        extractor = TweetTextExtractor(tweet_with_text_only)
        result = extractor.extract_text()
        
        self.assertEqual(result[0]['text'], "This is the text field")

    def test_extract_text_with_empty_input(self):
        """Test extraction with empty tweet list"""
        extractor = TweetTextExtractor([])
        result = extractor.extract_text()
        
        self.assertEqual(len(result), 0)

    def test_extract_text_preserves_all_fields(self):
        """Test that all required fields are preserved in extraction"""
        extractor = TweetTextExtractor(self.uk_tweets[:1])
        result = extractor.extract_text()
        
        tweet = result[0]
        required_fields = ['date', 'text', 'coordinates', 'place', 'source', 'created_at']
        
        for field in required_fields:
            self.assertIn(field, tweet)

    def test_processed_tweets_attribute(self):
        """Test that processed_tweets attribute is properly set"""
        extractor = TweetTextExtractor(self.uk_tweets)
        self.assertEqual(len(extractor.processed_tweets), 0)  # Initially empty
        
        result = extractor.extract_text()
        self.assertEqual(len(extractor.processed_tweets), 2)  # Populated after extraction
        self.assertEqual(extractor.processed_tweets, result)

    def test_class_attributes_exist(self):
        """Test that class has expected attributes"""
        extractor = TweetTextExtractor([])
        self.assertTrue(hasattr(extractor, 'tweet_json'))
        self.assertTrue(hasattr(extractor, 'processed_tweets'))
        self.assertTrue(hasattr(extractor, 'extract_text'))

    def test_text_field_fallback_priority(self):
        """Test that full_text is preferred over text field"""
        tweet_with_both = [{
            "created_at": "Wed Oct 11 10:30:00 +0000 2023",
            "full_text": "This is the full text",
            "text": "This is the truncated text",
            "coordinates": None,
            "place": None,
            "source": "test"
        }]
        
        extractor = TweetTextExtractor(tweet_with_both)
        result = extractor.extract_text()
        
        # Should prefer full_text over text
        self.assertEqual(result[0]['text'], "This is the full text")


if __name__ == '__main__':
    unittest.main()