"""
Unit tests for TwitterShillHunter main class with mocked Twitter/X API
"""
import unittest
from unittest.mock import patch, MagicMock, Mock
from twitter_shill_hunter.twitter_shill_hunter import TwitterShillHunter
from tests.mock_data import SAMPLE_CONFIG, UK_ENGLISH_TWEETS, US_ENGLISH_TWEETS, MIXED_TWEETS


class MockTweepyStatus:
    """Mock class to simulate tweepy Status objects"""
    def __init__(self, tweet_data):
        self._json = tweet_data


class TestTwitterShillHunter(unittest.TestCase):
    """Test cases for TwitterShillHunter main class with mocked Twitter API"""

    def setUp(self):
        """Set up test fixtures"""
        self.sample_config = SAMPLE_CONFIG
        self.sample_plugins = {
            'twitter_shill_hunter.processors': ['sentiment_analysis', 'grammar_analysis']
        }

    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.API')
    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.OAuth1UserHandler')
    @patch('twitter_shill_hunter.twitter_shill_hunter.pkg_resources.load_entry_point')
    def test_initialization_with_mocked_api(self, mock_load_entry_point, mock_oauth, mock_api):
        """Test TwitterShillHunter initialization with mocked Twitter API"""
        # Mock OAuth handler
        mock_auth = MagicMock()
        mock_oauth.return_value = mock_auth
        
        # Mock API instance
        mock_api_instance = MagicMock()
        mock_api.return_value = mock_api_instance
        
        # Mock tweet statuses
        mock_statuses = [MockTweepyStatus(tweet) for tweet in UK_ENGLISH_TWEETS]
        mock_api_instance.user_timeline.return_value = mock_statuses
        
        # Mock processors
        mock_processor_class = MagicMock()
        mock_load_entry_point.return_value = mock_processor_class
        
        # Create TwitterShillHunter instance
        hunter = TwitterShillHunter(self.sample_config, self.sample_plugins)
        
        # Verify authentication was set up correctly
        mock_oauth.assert_called_once_with(
            'test_consumer_key', 'test_consumer_secret',
            'test_access_token', 'test_access_secret'
        )
        mock_api.assert_called_once_with(mock_auth, wait_on_rate_limit=True)
        
        # Verify configuration was loaded correctly
        self.assertEqual(hunter.access_token, 'test_access_token')
        self.assertEqual(hunter.access_secret, 'test_access_secret')
        self.assertEqual(hunter.consumer_key, 'test_consumer_key')
        self.assertEqual(hunter.consumer_secret, 'test_consumer_secret')
        self.assertEqual(hunter.target, 'test_user')
        self.assertEqual(hunter.search_terms, ['test', 'example', 'sample'])
        self.assertEqual(hunter.dialect, 'en-US')

    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.API')
    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.OAuth1UserHandler')
    @patch('twitter_shill_hunter.twitter_shill_hunter.pkg_resources.load_entry_point')
    def test_load_plugins(self, mock_load_entry_point, mock_oauth, mock_api):
        """Test plugin loading functionality"""
        # Mock authentication components
        mock_oauth.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api.return_value = mock_api_instance
        mock_api_instance.user_timeline.return_value = []
        
        # Mock processor classes
        mock_sentiment_processor = MagicMock()
        mock_grammar_processor = MagicMock()
        
        def mock_load_entry_point_side_effect(package, category, plugin):
            if plugin == 'sentiment_analysis':
                return mock_sentiment_processor
            elif plugin == 'grammar_analysis':
                return mock_grammar_processor
            return MagicMock()
        
        mock_load_entry_point.side_effect = mock_load_entry_point_side_effect
        
        hunter = TwitterShillHunter(self.sample_config, self.sample_plugins)
        
        # Verify plugins were loaded
        self.assertIn('sentiment_analysis', hunter.loaded_processor_plugin_dict)
        self.assertIn('grammar_analysis', hunter.loaded_processor_plugin_dict)
        self.assertEqual(hunter.loaded_processor_plugin_dict['sentiment_analysis'], mock_sentiment_processor)
        self.assertEqual(hunter.loaded_processor_plugin_dict['grammar_analysis'], mock_grammar_processor)

    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.API')
    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.OAuth1UserHandler')
    @patch('twitter_shill_hunter.twitter_shill_hunter.pkg_resources.load_entry_point')
    def test_initiate_api_with_uk_tweets(self, mock_load_entry_point, mock_oauth, mock_api):
        """Test API initialization and tweet fetching with UK English tweets"""
        # Mock authentication
        mock_oauth.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api.return_value = mock_api_instance
        
        # Mock UK English tweets
        mock_statuses = [MockTweepyStatus(tweet) for tweet in UK_ENGLISH_TWEETS]
        mock_api_instance.user_timeline.return_value = mock_statuses
        
        # Mock processors
        mock_processor_class = MagicMock()
        mock_processor_instance = MagicMock()
        mock_processor_class.return_value = mock_processor_instance
        mock_load_entry_point.return_value = mock_processor_class
        
        hunter = TwitterShillHunter(self.sample_config, self.sample_plugins)
        
        # Verify user_timeline was called with correct parameters
        mock_api_instance.user_timeline.assert_called_once_with(
            screen_name='test_user',
            exclude_replies=True,
            include_rts=False,
            count=200,
            tweet_mode='extended'
        )

    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.API')
    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.OAuth1UserHandler')
    @patch('twitter_shill_hunter.twitter_shill_hunter.pkg_resources.load_entry_point')
    def test_initiate_api_with_us_tweets(self, mock_load_entry_point, mock_oauth, mock_api):
        """Test API initialization and tweet fetching with US English tweets"""
        # Mock authentication
        mock_oauth.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api.return_value = mock_api_instance
        
        # Mock US English tweets
        mock_statuses = [MockTweepyStatus(tweet) for tweet in US_ENGLISH_TWEETS]
        mock_api_instance.user_timeline.return_value = mock_statuses
        
        # Mock processors
        mock_processor_class = MagicMock()
        mock_load_entry_point.return_value = mock_processor_class
        
        hunter = TwitterShillHunter(self.sample_config, self.sample_plugins)
        
        # Verify the process completed without error
        self.assertIsNotNone(hunter.api)

    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.API')
    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.OAuth1UserHandler')
    @patch('twitter_shill_hunter.twitter_shill_hunter.pkg_resources.load_entry_point')
    def test_initiate_api_with_mixed_tweets(self, mock_load_entry_point, mock_oauth, mock_api):
        """Test API initialization with mixed UK/US English tweets"""
        # Mock authentication
        mock_oauth.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api.return_value = mock_api_instance
        
        # Mock mixed tweets
        mock_statuses = [MockTweepyStatus(tweet) for tweet in MIXED_TWEETS]
        mock_api_instance.user_timeline.return_value = mock_statuses
        
        # Mock processors
        mock_processor_class = MagicMock()
        mock_load_entry_point.return_value = mock_processor_class
        
        hunter = TwitterShillHunter(self.sample_config, self.sample_plugins)
        
        # Verify initialization completed
        self.assertIsNotNone(hunter.api)
        self.assertEqual(len(hunter.loaded_processor_plugin_dict), 2)

    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.API')
    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.OAuth1UserHandler')
    @patch('twitter_shill_hunter.twitter_shill_hunter.pkg_resources.load_entry_point')
    def test_api_exception_handling(self, mock_load_entry_point, mock_oauth, mock_api):
        """Test handling of API exceptions"""
        # Mock authentication
        mock_oauth.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api.return_value = mock_api_instance
        
        # Mock API exception
        mock_api_instance.user_timeline.side_effect = Exception("API Error")
        
        # Mock processors
        mock_processor_class = MagicMock()
        mock_load_entry_point.return_value = mock_processor_class
        
        # Should not raise exception - should be caught and handled
        try:
            hunter = TwitterShillHunter(self.sample_config, self.sample_plugins)
            # If we get here, the exception was handled properly
            self.assertIsNotNone(hunter.api)
        except Exception as e:
            self.fail(f"TwitterShillHunter should handle API exceptions gracefully, but raised: {e}")

    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.API')
    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.OAuth1UserHandler')
    @patch('twitter_shill_hunter.twitter_shill_hunter.pkg_resources.load_entry_point')
    def test_load_processors_with_dynamic_args(self, mock_load_entry_point, mock_oauth, mock_api):
        """Test load_processors method with dynamic argument passing"""
        # Mock authentication
        mock_oauth.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api.return_value = mock_api_instance
        mock_api_instance.user_timeline.return_value = []
        
        # Mock processor with specific process_data signature
        mock_processor_class = MagicMock()
        mock_processor_instance = MagicMock()
        mock_processor_class.return_value = mock_processor_instance
        
        # Mock inspect.getfullargspec to return specific arguments
        with patch('twitter_shill_hunter.twitter_shill_hunter.inspect.getfullargspec') as mock_getfullargspec:
            # Mock the function signature inspection
            mock_argspec = MagicMock()
            mock_argspec.args = ['self', 'tweets_and_date', 'search_terms', 'dialect']
            mock_getfullargspec.return_value = mock_argspec
            
            mock_load_entry_point.return_value = mock_processor_class
            
            hunter = TwitterShillHunter(self.sample_config, self.sample_plugins)
            
            # Verify process_data was called on processor instances
            # (The actual call happens during initialization via load_processors)
            mock_processor_class.assert_called()

    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.API')
    @patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.OAuth1UserHandler')
    @patch('twitter_shill_hunter.twitter_shill_hunter.pkg_resources.load_entry_point')
    def test_empty_tweet_response(self, mock_load_entry_point, mock_oauth, mock_api):
        """Test handling of empty tweet response from API"""
        # Mock authentication
        mock_oauth.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api.return_value = mock_api_instance
        
        # Mock empty tweet response
        mock_api_instance.user_timeline.return_value = []
        
        # Mock processors
        mock_processor_class = MagicMock()
        mock_load_entry_point.return_value = mock_processor_class
        
        hunter = TwitterShillHunter(self.sample_config, self.sample_plugins)
        
        # Should handle empty response gracefully
        self.assertIsNotNone(hunter.api)

    def test_class_attributes(self):
        """Test that class attributes are properly defined"""
        # Test class attributes exist (before instantiation)
        self.assertTrue(hasattr(TwitterShillHunter, 'access_token'))
        self.assertTrue(hasattr(TwitterShillHunter, 'access_secret'))
        self.assertTrue(hasattr(TwitterShillHunter, 'consumer_key'))
        self.assertTrue(hasattr(TwitterShillHunter, 'consumer_secret'))
        self.assertTrue(hasattr(TwitterShillHunter, 'target'))
        self.assertTrue(hasattr(TwitterShillHunter, 'api'))
        self.assertTrue(hasattr(TwitterShillHunter, 'search_terms'))
        self.assertTrue(hasattr(TwitterShillHunter, 'dialect'))
        self.assertTrue(hasattr(TwitterShillHunter, 'processors_plugin'))
        self.assertTrue(hasattr(TwitterShillHunter, 'loaded_processor_plugin_dict'))


if __name__ == '__main__':
    unittest.main()