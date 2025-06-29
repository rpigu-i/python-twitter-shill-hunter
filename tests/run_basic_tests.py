"""
Simple test suite that can run without external dependencies
"""
import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.dirname(__file__))

from test_tweet_text_extractor import TestTweetTextExtractor
from test_input import TestProcessInputYaml
from test_geo_analysis import TestGeoAnalysis

def run_basic_tests():
    """Run tests that don't require external dependencies"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases that don't require external libraries
    suite.addTest(loader.loadTestsFromTestCase(TestTweetTextExtractor))
    suite.addTest(loader.loadTestsFromTestCase(TestProcessInputYaml))
    suite.addTest(loader.loadTestsFromTestCase(TestGeoAnalysis))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_basic_tests()
    print(f"\nBasic tests completed: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)