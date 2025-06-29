#!/usr/bin/env python3
"""
Test runner for Twitter Shill Hunter unit tests
"""
import unittest
import sys
import os

# Add the src directory and tests directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.dirname(__file__))

# Import all test classes explicitly
from test_tweet_text_extractor import TestTweetTextExtractor
from test_input import TestProcessInputYaml
from test_geo_analysis import TestGeoAnalysis

# Import test classes that require external dependencies
# These will fail if dependencies are not installed, but import errors are resolved
try:
    from test_grammar_analysis import TestGrammarAnalysis
    grammar_analysis_available = True
except ImportError as e:
    print(f"Warning: Could not import grammar analysis tests: {e}")
    grammar_analysis_available = False

try:
    from test_spelling_analysis import TestSpellingAnalysis
    spelling_analysis_available = True
except ImportError as e:
    print(f"Warning: Could not import spelling analysis tests: {e}")
    spelling_analysis_available = False

try:
    from test_sentiment_analysis import TestSentimentAnalysis
    sentiment_analysis_available = True
except ImportError as e:
    print(f"Warning: Could not import sentiment analysis tests: {e}")
    sentiment_analysis_available = False

try:
    from test_twitter_shill_hunter import TestTwitterShillHunter
    twitter_shill_hunter_available = True
except ImportError as e:
    print(f"Warning: Could not import twitter shill hunter tests: {e}")
    twitter_shill_hunter_available = False

def run_tests():
    """Run all unit tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add basic test cases that don't require external libraries
    suite.addTest(loader.loadTestsFromTestCase(TestTweetTextExtractor))
    suite.addTest(loader.loadTestsFromTestCase(TestProcessInputYaml))
    suite.addTest(loader.loadTestsFromTestCase(TestGeoAnalysis))
    
    # Add test cases that require external dependencies (if available)
    if grammar_analysis_available:
        suite.addTest(loader.loadTestsFromTestCase(TestGrammarAnalysis))
    
    if spelling_analysis_available:
        suite.addTest(loader.loadTestsFromTestCase(TestSpellingAnalysis))
    
    if sentiment_analysis_available:
        suite.addTest(loader.loadTestsFromTestCase(TestSentimentAnalysis))
    
    if twitter_shill_hunter_available:
        suite.addTest(loader.loadTestsFromTestCase(TestTwitterShillHunter))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)