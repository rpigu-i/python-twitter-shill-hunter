"""
Unit tests for ProcessInputYaml class
"""
import unittest
import tempfile
import os
import yaml
from twitter_shill_hunter.input import ProcessInputYaml
from mock_data import SAMPLE_CONFIG


class TestProcessInputYaml(unittest.TestCase):
    """Test cases for ProcessInputYaml"""

    def setUp(self):
        """Set up test fixtures"""
        self.processor = ProcessInputYaml()
        self.sample_config = SAMPLE_CONFIG

    def test_yaml_processor_with_valid_file(self):
        """Test processing a valid YAML file"""
        # Create a temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            yaml.dump(self.sample_config, temp_file)
            temp_file_path = temp_file.name

        try:
            result = self.processor.yaml_processor(temp_file_path)
            
            self.assertIsInstance(result, dict)
            self.assertEqual(result['config']['target'], 'test_user')
            self.assertEqual(result['config']['dialect'], 'en-US')
            self.assertEqual(result['config']['search_terms'], ['test', 'example', 'sample'])
            
        finally:
            os.unlink(temp_file_path)

    def test_yaml_processor_with_complex_config(self):
        """Test processing a more complex YAML configuration"""
        complex_config = {
            "config": {
                "access_token": "complex_token_123",
                "access_secret": "complex_secret_456",
                "consumer_key": "complex_key_789", 
                "consumer_secret": "complex_consumer_secret",
                "target": "complex_user",
                "search_terms": ["politics", "economics", "social", "environment"],
                "dialect": "en-GB"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            yaml.dump(complex_config, temp_file)
            temp_file_path = temp_file.name

        try:
            result = self.processor.yaml_processor(temp_file_path)
            
            self.assertEqual(result['config']['dialect'], 'en-GB')
            self.assertEqual(len(result['config']['search_terms']), 4)
            self.assertIn('politics', result['config']['search_terms'])
            
        finally:
            os.unlink(temp_file_path)

    def test_yaml_processor_file_not_found(self):
        """Test processing a non-existent file raises FileNotFoundError"""
        with self.assertRaises(FileNotFoundError):
            self.processor.yaml_processor('non_existent_file.yaml')

    def test_yaml_processor_with_empty_file(self):
        """Test processing an empty YAML file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            # Write nothing to create an empty file
            temp_file_path = temp_file.name

        try:
            result = self.processor.yaml_processor(temp_file_path)
            self.assertIsNone(result)
            
        finally:
            os.unlink(temp_file_path)

    def test_yaml_processor_with_invalid_yaml(self):
        """Test processing invalid YAML content raises YAMLError"""
        invalid_yaml_content = """
        config:
          target: test_user
          invalid_structure: [
            - missing closing bracket
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(invalid_yaml_content)
            temp_file_path = temp_file.name

        try:
            with self.assertRaises(yaml.YAMLError):
                self.processor.yaml_processor(temp_file_path)
            
        finally:
            os.unlink(temp_file_path)

    def test_yaml_processor_return_type(self):
        """Test that yaml_processor returns the correct type"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            yaml.dump(self.sample_config, temp_file)
            temp_file_path = temp_file.name

        try:
            result = self.processor.yaml_processor(temp_file_path)
            self.assertIsInstance(result, dict)
            
        finally:
            os.unlink(temp_file_path)

    def test_yaml_processor_nested_structure(self):
        """Test processing YAML with nested structures"""
        nested_config = {
            "config": {
                "api_keys": {
                    "access_token": "token",
                    "access_secret": "secret"
                },
                "target_info": {
                    "username": "test_user",
                    "location": "US"
                },
                "analysis_options": {
                    "search_terms": ["term1", "term2"],
                    "dialect": "en-US",
                    "advanced": {
                        "deep_analysis": True,
                        "threshold": 0.8
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            yaml.dump(nested_config, temp_file)
            temp_file_path = temp_file.name

        try:
            result = self.processor.yaml_processor(temp_file_path)
            
            self.assertEqual(result['config']['target_info']['username'], 'test_user')
            self.assertEqual(result['config']['analysis_options']['advanced']['threshold'], 0.8)
            self.assertTrue(result['config']['analysis_options']['advanced']['deep_analysis'])
            
        finally:
            os.unlink(temp_file_path)


if __name__ == '__main__':
    unittest.main()