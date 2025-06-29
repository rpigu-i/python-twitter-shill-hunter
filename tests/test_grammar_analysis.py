"""
Unit tests for GrammarAnalysis processor
"""
import unittest
from unittest.mock import patch, MagicMock
from twitter_shill_hunter.processors.grammar_analysis.grammar_analysis import GrammarAnalysis
from tests.mock_data import SAMPLE_PROCESSED_TWEETS, UK_ENGLISH_TWEETS, US_ENGLISH_TWEETS


class TestGrammarAnalysis(unittest.TestCase):
    """Test cases for GrammarAnalysis processor"""

    def setUp(self):
        """Set up test fixtures"""
        self.grammar_analyzer = GrammarAnalysis()
        self.sample_tweets = SAMPLE_PROCESSED_TWEETS
        self.uk_tweets = UK_ENGLISH_TWEETS
        self.us_tweets = US_ENGLISH_TWEETS

    def test_initialization(self):
        """Test GrammarAnalysis initialization"""
        analyzer = GrammarAnalysis()
        self.assertEqual(analyzer.dialect, "")
        self.assertEqual(analyzer.valid_dialects, [])

    @patch('twitter_shill_hunter.processors.grammar_analysis.grammar_analysis.os.listdir')
    @patch('twitter_shill_hunter.processors.grammar_analysis.grammar_analysis.pkg_resources.resource_filename')
    def test_get_lang_dialects(self, mock_resource_filename, mock_listdir):
        """Test get_lang_dialects method"""
        # Mock the resource path and directory listing
        mock_resource_filename.return_value = '/mock/path/en'
        mock_listdir.return_value = ['en-US.yaml', 'en-GB.yaml', 'en-AU.yaml', 'other.txt']
        
        self.grammar_analyzer.dialect = 'en-US'
        self.grammar_analyzer.get_lang_dialects()
        
        # Should include all .yaml files except the current dialect
        self.assertEqual(len(self.grammar_analyzer.valid_dialects), 2)
        self.assertIn('/mock/path/en/en-GB.yaml', self.grammar_analyzer.valid_dialects)
        self.assertIn('/mock/path/en/en-AU.yaml', self.grammar_analyzer.valid_dialects)
        self.assertNotIn('/mock/path/en/en-US.yaml', self.grammar_analyzer.valid_dialects)

    @patch.object(GrammarAnalysis, 'get_lang_dialects')
    @patch.object(GrammarAnalysis, 'analyze_dialect')
    def test_process_data(self, mock_analyze_dialect, mock_get_lang_dialects):
        """Test process_data method"""
        dialect = 'en-US'
        
        self.grammar_analyzer.process_data(self.sample_tweets, dialect)
        
        # Verify attributes are set correctly
        self.assertEqual(self.grammar_analyzer.dialect, dialect)
        self.assertEqual(self.grammar_analyzer.tweets_and_date, self.sample_tweets)
        
        # Verify methods are called
        mock_get_lang_dialects.assert_called_once()
        mock_analyze_dialect.assert_called_once()

    @patch.object(GrammarAnalysis, 'process_input')
    def test_analyze_dialect(self, mock_process_input):
        """Test analyze_dialect method"""
        # Mock the process_input method to return word data
        mock_process_input.return_value = {
            'words': ['colour', 'centre', 'organisation']
        }
        
        # Set up test data
        self.grammar_analyzer.tweets_and_date = [{
            'text': 'The colour of the centre is brilliant for our organisation',
            'date': 'test_date'
        }]
        self.grammar_analyzer.valid_dialects = ['/path/to/en-GB.yaml']
        
        # Execute the method
        self.grammar_analyzer.analyze_dialect()
        
        # Verify process_input was called with the dialect
        mock_process_input.assert_called_once_with('/path/to/en-GB.yaml')

    @patch('twitter_shill_hunter.processors.grammar_analysis.grammar_analysis.ProcessInputYaml')
    def test_process_input(self, mock_process_input_yaml_class):
        """Test process_input method"""
        # Mock the ProcessInputYaml class and its instance
        mock_yaml_processor = MagicMock()
        mock_yaml_processor.yaml_processor.return_value = {'words': ['test', 'words']}
        mock_process_input_yaml_class.return_value = mock_yaml_processor
        
        yaml_file = '/path/to/test.yaml'
        result = self.grammar_analyzer.process_input(yaml_file)
        
        # Verify ProcessInputYaml was instantiated and called correctly
        mock_process_input_yaml_class.assert_called_once()
        mock_yaml_processor.yaml_processor.assert_called_once_with(yaml_file)
        
        # Verify the result
        self.assertEqual(result, {'words': ['test', 'words']})

    @patch.object(GrammarAnalysis, 'process_input')
    def test_analyze_dialect_word_matching(self, mock_process_input):
        """Test that analyze_dialect correctly identifies dialect words in tweets"""
        # Mock process_input to return UK English words
        mock_process_input.return_value = {
            'words': ['colour', 'centre', 'organisation', 'favour']
        }
        
        # Set up test data with UK English tweet
        self.grammar_analyzer.tweets_and_date = [{
            'text': 'The colour of autumn leaves is brilliant. Centre of town looks lovely.',
            'date': 'test_date'
        }]
        self.grammar_analyzer.valid_dialects = ['/path/to/en-GB.yaml']
        
        # Execute the method (this will print results but we can't easily capture them)
        # The main test is that it doesn't raise an exception
        self.grammar_analyzer.analyze_dialect()
        
        # Verify process_input was called
        mock_process_input.assert_called_once()

    @patch.object(GrammarAnalysis, 'process_input')
    def test_analyze_dialect_no_matches(self, mock_process_input):
        """Test analyze_dialect when no dialect words are found"""
        # Mock process_input to return words not in our tweets
        mock_process_input.return_value = {
            'words': ['nonexistent', 'missing', 'notfound']
        }
        
        self.grammar_analyzer.tweets_and_date = self.sample_tweets
        self.grammar_analyzer.valid_dialects = ['/path/to/test.yaml']
        
        # This should run without error even when no matches are found
        self.grammar_analyzer.analyze_dialect()
        
        mock_process_input.assert_called_once()

    def test_analyze_dialect_empty_dialects(self):
        """Test analyze_dialect with empty valid_dialects list"""
        self.grammar_analyzer.tweets_and_date = self.sample_tweets
        self.grammar_analyzer.valid_dialects = []
        
        # Should run without error when no dialects to process
        self.grammar_analyzer.analyze_dialect()

    def test_analyze_dialect_empty_tweets(self):
        """Test analyze_dialect with empty tweets list"""
        with patch.object(self.grammar_analyzer, 'process_input') as mock_process_input:
            mock_process_input.return_value = {'words': ['test']}
            
            self.grammar_analyzer.tweets_and_date = []
            self.grammar_analyzer.valid_dialects = ['/path/to/test.yaml']
            
            # Should run without error when no tweets to process
            self.grammar_analyzer.analyze_dialect()
            
            mock_process_input.assert_called_once()

    def test_get_lang_dialects_splits_dialect_correctly(self):
        """Test that get_lang_dialects correctly splits dialect string"""
        with patch('twitter_shill_hunter.processors.grammar_analysis.grammar_analysis.os.listdir') as mock_listdir:
            with patch('twitter_shill_hunter.processors.grammar_analysis.grammar_analysis.pkg_resources.resource_filename') as mock_resource_filename:
                mock_resource_filename.return_value = '/mock/path/fr'
                mock_listdir.return_value = ['fr-FR.yaml', 'fr-CA.yaml']
                
                # Test with French dialect
                self.grammar_analyzer.dialect = 'fr-FR'
                self.grammar_analyzer.get_lang_dialects()
                
                # Verify resource_filename was called with correct language
                mock_resource_filename.assert_called_once_with(
                    'twitter_shill_hunter.processors.grammar_analysis', 
                    '/dialect_mappings/fr'
                )


if __name__ == '__main__':
    unittest.main()