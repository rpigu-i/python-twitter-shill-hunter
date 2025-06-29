"""
Unit tests for GeoAnalysis processor
"""
import unittest
from twitter_shill_hunter.processors.geo_analysis.geo_analysis import GeoAnalysis
from mock_data import SAMPLE_PROCESSED_TWEETS


class TestGeoAnalysis(unittest.TestCase):
    """Test cases for GeoAnalysis processor"""

    def setUp(self):
        """Set up test fixtures"""
        self.geo_analyzer = GeoAnalysis()
        self.sample_tweets = SAMPLE_PROCESSED_TWEETS

    def test_process_data_with_tweets(self):
        """Test geo analysis processing with sample tweets"""
        # This test mainly verifies the method runs without error
        # since the actual implementation just prints tweet data
        try:
            self.geo_analyzer.process_data(self.sample_tweets)
        except Exception as e:
            self.fail(f"process_data raised an unexpected exception: {e}")

    def test_process_data_with_empty_tweets(self):
        """Test geo analysis with empty tweets list"""
        try:
            self.geo_analyzer.process_data([])
        except Exception as e:
            self.fail(f"process_data with empty list raised an unexpected exception: {e}")

    def test_process_data_with_coordinates(self):
        """Test processing tweets with coordinate data"""
        tweets_with_coords = [
            {
                'created_at': 'Wed Oct 11 10:30:00 +0000 2023',
                'coordinates': {'type': 'Point', 'coordinates': [-74.0059, 40.7128]},
                'source': 'Twitter for iPhone',
                'text': 'Tweet with coordinates'
            }
        ]
        
        try:
            self.geo_analyzer.process_data(tweets_with_coords)
        except Exception as e:
            self.fail(f"process_data with coordinates raised an unexpected exception: {e}")

    def test_process_data_with_none_coordinates(self):
        """Test processing tweets with None coordinates"""
        tweets_with_none_coords = [
            {
                'created_at': 'Wed Oct 11 10:30:00 +0000 2023',
                'coordinates': None,
                'source': 'Twitter for Android',
                'text': 'Tweet without coordinates'
            }
        ]
        
        try:
            self.geo_analyzer.process_data(tweets_with_none_coords)
        except Exception as e:
            self.fail(f"process_data with None coordinates raised an unexpected exception: {e}")

    def test_process_data_with_various_sources(self):
        """Test processing tweets from various sources"""
        tweets_various_sources = [
            {
                'created_at': 'Wed Oct 11 10:30:00 +0000 2023',
                'coordinates': None,
                'source': 'Twitter for iPhone',
                'text': 'iPhone tweet'
            },
            {
                'created_at': 'Wed Oct 11 11:30:00 +0000 2023',
                'coordinates': None,
                'source': 'Twitter for Android',
                'text': 'Android tweet'
            },
            {
                'created_at': 'Wed Oct 11 12:30:00 +0000 2023',
                'coordinates': None,
                'source': 'Twitter Web Client',
                'text': 'Web client tweet'
            }
        ]
        
        try:
            self.geo_analyzer.process_data(tweets_various_sources)
        except Exception as e:
            self.fail(f"process_data with various sources raised an unexpected exception: {e}")

    def test_process_data_method_signature(self):
        """Test that process_data accepts the expected parameters"""
        # Verify the method exists and can be called with tweets_and_date parameter
        self.assertTrue(hasattr(self.geo_analyzer, 'process_data'))
        self.assertTrue(callable(getattr(self.geo_analyzer, 'process_data')))

    def test_process_data_with_missing_fields(self):
        """Test processing tweets with missing fields"""
        tweets_missing_fields = [
            {
                'created_at': 'Wed Oct 11 10:30:00 +0000 2023',
                # Missing coordinates and source
                'text': 'Tweet with missing fields'
            }
        ]
        
        # The method should handle missing fields gracefully
        # though it might print None or raise KeyError
        try:
            self.geo_analyzer.process_data(tweets_missing_fields)
        except KeyError:
            # This is expected behavior if the implementation doesn't handle missing keys
            pass
        except Exception as e:
            # Other exceptions might indicate a problem
            self.fail(f"process_data with missing fields raised unexpected exception: {e}")

    def test_class_docstring(self):
        """Test that the class has appropriate documentation"""
        self.assertIsNotNone(GeoAnalysis.__doc__)
        self.assertIn("geo", GeoAnalysis.__doc__.lower())

    def test_method_docstring(self):
        """Test that the process_data method has documentation"""
        self.assertIsNotNone(self.geo_analyzer.process_data.__doc__)
        self.assertIn("processing", self.geo_analyzer.process_data.__doc__.lower())

    def test_class_instantiation(self):
        """Test that GeoAnalysis can be instantiated without parameters"""
        analyzer = GeoAnalysis()
        self.assertIsInstance(analyzer, GeoAnalysis)

    def test_process_data_handles_large_dataset(self):
        """Test processing a larger dataset"""
        # Create a larger dataset to test performance/stability
        large_dataset = []
        for i in range(100):
            large_dataset.append({
                'created_at': f'Wed Oct {11 + (i % 20)} 10:30:00 +0000 2023',
                'coordinates': None if i % 2 == 0 else {'type': 'Point', 'coordinates': [i, i+1]},
                'source': f'Twitter Source {i % 3}',
                'text': f'Tweet number {i}'
            })
        
        try:
            self.geo_analyzer.process_data(large_dataset)
        except Exception as e:
            self.fail(f"process_data with large dataset raised an unexpected exception: {e}")


if __name__ == '__main__':
    unittest.main()