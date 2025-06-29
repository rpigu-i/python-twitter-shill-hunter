"""
Unit tests for SentimentAnalysis processor
"""
import unittest
from unittest.mock import patch, MagicMock
from twitter_shill_hunter.processors.sentiment_analysis.sentiment_analysis import SentimentAnalysis
from tests.mock_data import SAMPLE_PROCESSED_TWEETS


class TestSentimentAnalysis(unittest.TestCase):
    """Test cases for SentimentAnalysis processor"""

    def setUp(self):
        """Set up test fixtures"""
        self.sentiment_analyzer = SentimentAnalysis()
        self.sample_tweets = SAMPLE_PROCESSED_TWEETS
        self.search_terms = ["color", "Organization", "test"]

    @patch('twitter_shill_hunter.processors.sentiment_analysis.sentiment_analysis.SentimentIntensityAnalyzer')
    def test_process_data_with_matching_terms(self, mock_sia_class):
        """Test sentiment analysis when search terms are found"""
        # Mock the SentimentIntensityAnalyzer
        mock_sia = MagicMock()
        mock_sia_class.return_value = mock_sia
        mock_sia.polarity_scores.return_value = {
            'neg': 0.0,
            'neu': 0.5,
            'pos': 0.5,
            'compound': 0.8
        }

        # Mock the aggregate_search_results method
        with patch.object(self.sentiment_analyzer, 'aggregate_search_results') as mock_aggregate:
            mock_aggregate.return_value = {'compound': 0.8}
            
            self.sentiment_analyzer.process_data(self.sample_tweets, self.search_terms)
            
            # Verify SentimentIntensityAnalyzer was called
            mock_sia_class.assert_called_once()
            
            # Verify polarity_scores was called for tweets with matching terms
            self.assertTrue(mock_sia.polarity_scores.called)
            
            # Verify aggregate_search_results was called
            mock_aggregate.assert_called_once_with(self.search_terms)

    @patch('twitter_shill_hunter.processors.sentiment_analysis.sentiment_analysis.SentimentIntensityAnalyzer')
    def test_process_data_no_matching_terms(self, mock_sia_class):
        """Test sentiment analysis when no search terms are found"""
        mock_sia = MagicMock()
        mock_sia_class.return_value = mock_sia
        
        # Use search terms that won't match our sample tweets
        no_match_terms = ["nonexistent", "notfound", "missing"]
        
        with patch.object(self.sentiment_analyzer, 'aggregate_search_results') as mock_aggregate:
            mock_aggregate.return_value = {'compound': 0.0}
            
            self.sentiment_analyzer.process_data(self.sample_tweets, no_match_terms)
            
            # Verify polarity_scores was not called since no terms matched
            mock_sia.polarity_scores.assert_not_called()

    def test_initialization(self):
        """Test SentimentAnalysis initialization"""
        analyzer = SentimentAnalysis()
        self.assertEqual(analyzer.aggregated_results, [])

    @patch('twitter_shill_hunter.processors.sentiment_analysis.sentiment_analysis.SentimentIntensityAnalyzer')
    def test_aggregated_results_populated(self, mock_sia_class):
        """Test that aggregated_results are populated correctly"""
        mock_sia = MagicMock()
        mock_sia_class.return_value = mock_sia
        mock_sia.polarity_scores.return_value = {
            'neg': 0.1,
            'neu': 0.3,
            'pos': 0.6,
            'compound': 0.7
        }

        with patch.object(self.sentiment_analyzer, 'aggregate_search_results') as mock_aggregate:
            mock_aggregate.return_value = {'compound': 0.7}
            
            self.sentiment_analyzer.process_data(self.sample_tweets, ["color"])
            
            # Check that aggregated_results contains the expected structure
            self.assertTrue(len(self.sentiment_analyzer.aggregated_results) > 0)
            
            # Verify the structure of aggregated results
            result = self.sentiment_analyzer.aggregated_results[0]
            expected_keys = ['date', 'tweet', 'search_terms', 'neg', 'neu', 'pos', 'compound']
            for key in expected_keys:
                self.assertIn(key, result)

    @patch('twitter_shill_hunter.processors.sentiment_analysis.sentiment_analysis.SentimentIntensityAnalyzer')
    def test_search_terms_found_tracking(self, mock_sia_class):
        """Test that found search terms are tracked correctly"""
        mock_sia = MagicMock()
        mock_sia_class.return_value = mock_sia
        mock_sia.polarity_scores.return_value = {
            'neg': 0.0,
            'neu': 0.4,
            'pos': 0.6,
            'compound': 0.8
        }

        with patch.object(self.sentiment_analyzer, 'aggregate_search_results') as mock_aggregate:
            mock_aggregate.return_value = {'compound': 0.8}
            
            # Test with terms that should be found in our sample tweets
            search_terms = ["color", "Organization"]
            self.sentiment_analyzer.process_data(self.sample_tweets, search_terms)
            
            # Check that at least one result was added
            self.assertTrue(len(self.sentiment_analyzer.aggregated_results) > 0)
            
            # Check that search terms were properly recorded
            result = self.sentiment_analyzer.aggregated_results[0]
            self.assertIn('search_terms', result)
            self.assertIsInstance(result['search_terms'], list)

    def test_empty_tweets_list(self):
        """Test processing with empty tweets list"""
        with patch.object(self.sentiment_analyzer, 'aggregate_search_results') as mock_aggregate:
            mock_aggregate.return_value = {'compound': 0.0}
            
            self.sentiment_analyzer.process_data([], self.search_terms)
            
            # Should have no aggregated results
            self.assertEqual(len(self.sentiment_analyzer.aggregated_results), 0)
            
            # aggregate_search_results should still be called
            mock_aggregate.assert_called_once_with(self.search_terms)

    def test_empty_search_terms(self):
        """Test processing with empty search terms"""
        with patch.object(self.sentiment_analyzer, 'aggregate_search_results') as mock_aggregate:
            mock_aggregate.return_value = {'compound': 0.0}
            
            self.sentiment_analyzer.process_data(self.sample_tweets, [])
            
            # Should have no aggregated results since no search terms provided
            self.assertEqual(len(self.sentiment_analyzer.aggregated_results), 0)


if __name__ == '__main__':
    unittest.main()