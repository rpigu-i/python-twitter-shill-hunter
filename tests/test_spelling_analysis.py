"""
Unit tests for SpellingAnalysis processor
"""
import unittest
from unittest.mock import patch, MagicMock
from twitter_shill_hunter.processors.spelling_analysis.spelling_analysis import SpellingAnalysis
from tests.mock_data import SAMPLE_PROCESSED_TWEETS, UK_ENGLISH_TWEETS, US_ENGLISH_TWEETS


class TestSpellingAnalysis(unittest.TestCase):
    """Test cases for SpellingAnalysis processor"""

    def setUp(self):
        """Set up test fixtures"""
        self.spelling_analyzer = SpellingAnalysis()
        self.sample_tweets = SAMPLE_PROCESSED_TWEETS
        self.uk_tweets_processed = [
            {
                'text': 'The colour of autumn leaves is absolutely brilliant this year. Centre of town looks lovely.',
                'date': 'Wed Oct 11 10:30:00 +0000 2023'
            }
        ]
        self.us_tweets_processed = [
            {
                'text': 'The color of fall leaves is absolutely amazing this year. Downtown looks beautiful.',
                'date': 'Wed Oct 11 10:30:00 +0000 2023'
            }
        ]

    @patch('twitter_shill_hunter.processors.spelling_analysis.spelling_analysis.language_check.LanguageTool')
    def test_process_data_with_uk_dialect(self, mock_language_tool_class):
        """Test spelling analysis with UK English dialect"""
        # Mock LanguageTool
        mock_scanner = MagicMock()
        mock_language_tool_class.return_value = mock_scanner
        
        # Mock a spelling error result
        mock_match = MagicMock()
        mock_match.context = "This is the context"
        mock_match.ruleId = "SPELLING_ERROR"
        mock_match.category = "Spelling"
        mock_match.replacements = ["replacement1", "replacement2"]
        mock_scanner.check.return_value = [mock_match]
        
        dialect = 'en-GB'
        self.spelling_analyzer.process_data(self.uk_tweets_processed, dialect)
        
        # Verify LanguageTool was instantiated with correct dialect
        mock_language_tool_class.assert_called_once_with(dialect)
        
        # Verify check was called for each tweet
        self.assertEqual(mock_scanner.check.call_count, len(self.uk_tweets_processed))

    @patch('twitter_shill_hunter.processors.spelling_analysis.spelling_analysis.language_check.LanguageTool')
    def test_process_data_with_us_dialect(self, mock_language_tool_class):
        """Test spelling analysis with US English dialect"""
        mock_scanner = MagicMock()
        mock_language_tool_class.return_value = mock_scanner
        mock_scanner.check.return_value = []  # No spelling errors
        
        dialect = 'en-US'
        self.spelling_analyzer.process_data(self.us_tweets_processed, dialect)
        
        # Verify LanguageTool was instantiated with correct dialect
        mock_language_tool_class.assert_called_once_with(dialect)
        
        # Verify check was called
        mock_scanner.check.assert_called()

    @patch('twitter_shill_hunter.processors.spelling_analysis.spelling_analysis.language_check.LanguageTool')
    def test_process_data_handles_unicode_text(self, mock_language_tool_class):
        """Test that process_data handles Unicode text correctly"""
        mock_scanner = MagicMock()
        mock_language_tool_class.return_value = mock_scanner
        mock_scanner.check.return_value = []
        
        # Tweet with Unicode characters
        unicode_tweets = [{
            'text': 'Hello world! 😀 This has émojis and áccents',
            'date': 'test_date'
        }]
        
        self.spelling_analyzer.process_data(unicode_tweets, 'en-US')
        
        # Verify the method completes without error
        mock_scanner.check.assert_called()
        
        # The text passed to check should have non-ASCII characters removed
        call_args = mock_scanner.check.call_args[0][0]
        # Should not contain emoji or accented characters
        self.assertNotIn('😀', call_args)
        self.assertNotIn('é', call_args)
        self.assertNotIn('á', call_args)

    @patch('twitter_shill_hunter.processors.spelling_analysis.spelling_analysis.language_check.LanguageTool')
    def test_process_data_handles_spelling_matches(self, mock_language_tool_class):
        """Test handling of spelling matches with context and replacements"""
        mock_scanner = MagicMock()
        mock_language_tool_class.return_value = mock_scanner
        
        # Create mock matches with various properties
        mock_match1 = MagicMock()
        mock_match1.context = "This is a test context"
        mock_match1.ruleId = "SPELLING_ERROR_1"
        mock_match1.category = "Spelling"
        mock_match1.replacements = ["correction1", "correction2"]
        
        mock_match2 = MagicMock()
        mock_match2.context = "Another context with símböls"  # Unicode context
        mock_match2.ruleId = "GRAMMAR_ERROR"
        mock_match2.category = "Grammar"
        mock_match2.replacements = []  # No replacements
        
        mock_scanner.check.return_value = [mock_match1, mock_match2]
        
        tweets = [{
            'text': 'This is a test tweet with potential errors',
            'date': 'test_date'
        }]
        
        self.spelling_analyzer.process_data(tweets, 'en-US')
        
        # Verify the method handles both matches without error
        mock_scanner.check.assert_called_once()

    @patch('twitter_shill_hunter.processors.spelling_analysis.spelling_analysis.language_check.LanguageTool')
    def test_process_data_empty_tweets(self, mock_language_tool_class):
        """Test process_data with empty tweets list"""
        mock_scanner = MagicMock()
        mock_language_tool_class.return_value = mock_scanner
        
        self.spelling_analyzer.process_data([], 'en-US')
        
        # LanguageTool should still be instantiated
        mock_language_tool_class.assert_called_once_with('en-US')
        
        # But check should not be called since no tweets
        mock_scanner.check.assert_not_called()

    @patch('twitter_shill_hunter.processors.spelling_analysis.spelling_analysis.language_check.LanguageTool')
    def test_process_data_handles_bytes_text(self, mock_language_tool_class):
        """Test that process_data handles bytes text correctly"""
        mock_scanner = MagicMock()
        mock_language_tool_class.return_value = mock_scanner
        mock_scanner.check.return_value = []
        
        # Tweet with text that might be bytes
        tweets = [{
            'text': 'Regular string text',
            'date': 'test_date'
        }]
        
        # Should handle normal string text without issues
        self.spelling_analyzer.process_data(tweets, 'en-US')
        mock_scanner.check.assert_called()

    @patch('twitter_shill_hunter.processors.spelling_analysis.spelling_analysis.language_check.LanguageTool')
    def test_process_data_handles_match_with_unicode_context(self, mock_language_tool_class):
        """Test handling matches with Unicode characters in context"""
        mock_scanner = MagicMock()
        mock_language_tool_class.return_value = mock_scanner
        
        # Mock match with Unicode in context and replacements
        mock_match = MagicMock()
        mock_match.context = "Conéxt with ünïcödé"
        mock_match.ruleId = "TEST_RULE"
        mock_match.category = "Test"
        mock_match.replacements = ["rëplacement1", "replacement2"]
        
        mock_scanner.check.return_value = [mock_match]
        
        tweets = [{
            'text': 'Test tweet',
            'date': 'test_date'
        }]
        
        # Should handle Unicode in context and replacements without error
        self.spelling_analyzer.process_data(tweets, 'en-US')
        
        mock_scanner.check.assert_called_once()

    @patch('twitter_shill_hunter.processors.spelling_analysis.spelling_analysis.language_check.LanguageTool')
    def test_process_data_no_replacements(self, mock_language_tool_class):
        """Test handling matches with no replacement suggestions"""
        mock_scanner = MagicMock()
        mock_language_tool_class.return_value = mock_scanner
        
        # Mock match with no replacements
        mock_match = MagicMock()
        mock_match.context = "Test context"
        mock_match.ruleId = "NO_REPLACEMENT_RULE"
        mock_match.category = "Test"
        mock_match.replacements = None  # No replacements available
        
        mock_scanner.check.return_value = [mock_match]
        
        tweets = [{
            'text': 'Test tweet',
            'date': 'test_date'
        }]
        
        # Should handle cases where no replacements are available
        self.spelling_analyzer.process_data(tweets, 'en-US')
        
        mock_scanner.check.assert_called_once()

    def test_process_data_multiple_tweets(self):
        """Test processing multiple tweets"""
        with patch('twitter_shill_hunter.processors.spelling_analysis.spelling_analysis.language_check.LanguageTool') as mock_lt:
            mock_scanner = MagicMock()
            mock_lt.return_value = mock_scanner
            mock_scanner.check.return_value = []
            
            multiple_tweets = [
                {'text': 'First tweet text', 'date': 'date1'},
                {'text': 'Second tweet text', 'date': 'date2'},
                {'text': 'Third tweet text', 'date': 'date3'}
            ]
            
            self.spelling_analyzer.process_data(multiple_tweets, 'en-US')
            
            # Should call check for each tweet
            self.assertEqual(mock_scanner.check.call_count, 3)


if __name__ == '__main__':
    unittest.main()