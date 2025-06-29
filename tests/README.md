# Twitter Shill Hunter Test Suite

This directory contains comprehensive unit tests for the Twitter Shill Hunter application, including mock Twitter/X API endpoints and sample tweets in UK and US English.

## Test Structure

The test suite includes the following components:

### Core Test Files

- **`test_twitter_shill_hunter.py`** - Tests for the main TwitterShillHunter class with mocked Twitter API
- **`test_tweet_text_extractor.py`** - Tests for the TweetTextExtractor class
- **`test_input.py`** - Tests for the ProcessInputYaml configuration processor
- **`test_geo_analysis.py`** - Tests for the GeoAnalysis processor
- **`test_sentiment_analysis.py`** - Tests for the SentimentAnalysis processor (with mocked dependencies)
- **`test_grammar_analysis.py`** - Tests for the GrammarAnalysis processor (with mocked dependencies)
- **`test_spelling_analysis.py`** - Tests for the SpellingAnalysis processor (with mocked dependencies)

### Mock Data and Utilities

- **`mock_data.py`** - Contains sample tweet data in UK and US English, plus configuration fixtures
- **`run_basic_tests.py`** - Test runner for core tests that don't require external dependencies
- **`run_tests.py`** - Comprehensive test runner for all tests

## Mock Data

The test suite includes comprehensive mock data:

### Sample Tweets

- **UK English tweets**: Features British spellings (colour, centre, organisation, favour)
- **US English tweets**: Features American spellings (color, downtown, organization, favor)
- **Mixed datasets**: Combinations for testing dialect analysis

### Mock Twitter API

The tests include a fully mocked Twitter/X API using `unittest.mock` that simulates:

- OAuth authentication flow
- Tweet timeline fetching
- Status objects with proper JSON structure
- Error handling and edge cases

### Configuration Data

- Sample YAML configuration files
- API credentials (mocked for testing)
- Various dialect settings
- Search term configurations

## Running Tests

### Basic Tests (No External Dependencies)

Run the core tests that don't require external libraries:

```bash
cd /path/to/twitter-shill-hunter
python tests/run_basic_tests.py
```

These tests cover:
- TweetTextExtractor functionality
- YAML configuration processing
- GeoAnalysis processor
- Basic data structures and workflows

### Full Test Suite

To run all tests (requires mocking of external dependencies):

```bash
cd /path/to/twitter-shill-hunter
python tests/run_tests.py
```

### Individual Test Files

Run specific test files:

```bash
cd /path/to/twitter-shill-hunter
python -m unittest tests.test_tweet_text_extractor -v
```

## Test Coverage

The test suite provides comprehensive coverage of:

### Core Functionality
- ✅ Tweet text extraction and processing
- ✅ YAML configuration file handling
- ✅ OAuth authentication flow (mocked)
- ✅ API data fetching and processing (mocked)

### Processor Classes
- ✅ Sentiment analysis with search term matching
- ✅ Grammar analysis with dialect detection
- ✅ Spelling analysis with language checking
- ✅ Geographic analysis of tweet metadata

### Data Handling
- ✅ Unicode text processing
- ✅ Empty data sets
- ✅ Malformed input handling
- ✅ Field validation and transformation

### UK/US English Testing
- ✅ British English spelling detection ("colour", "centre", "organisation")
- ✅ American English spelling detection ("color", "downtown", "organization")
- ✅ Mixed dialect analysis
- ✅ Grammar pattern recognition

## Mock Twitter API Implementation

The test suite includes a sophisticated mock of the Twitter/X API:

### Authentication Mocking
```python
@patch('twitter_shill_hunter.twitter_shill_hunter.tweepy.OAuth1UserHandler')
def test_authentication(self, mock_oauth):
    # Mocks OAuth flow without requiring real credentials
```

### Tweet Data Mocking
```python
class MockTweepyStatus:
    """Mock class to simulate tweepy Status objects"""
    def __init__(self, tweet_data):
        self._json = tweet_data
```

### API Response Simulation
- User timeline fetching
- Tweet metadata extraction
- Error condition handling
- Rate limiting scenarios

## Test Isolation

Each test is properly isolated:

- **Fixtures**: Clean test data for each test case
- **Mocking**: External dependencies are mocked to prevent side effects
- **State Management**: Class variables are reset between tests where needed

## Sample Test Output

```
test_extract_text_with_uk_tweets ... ok
test_extract_text_with_us_tweets ... ok
test_yaml_processor_with_valid_file ... ok
test_initiate_api_with_mixed_tweets ... ok

----------------------------------------------------------------------
Ran 28 tests in 0.009s

OK
```

## Adding New Tests

When adding new tests:

1. **Import mock data**: Use data from `mock_data.py`
2. **Mock external dependencies**: Use `unittest.mock.patch` for external libraries
3. **Include UK/US samples**: Ensure dialect-specific testing where relevant
4. **Test error conditions**: Include edge cases and error scenarios
5. **Maintain isolation**: Ensure tests don't interfere with each other

## Dependencies for Full Testing

While the basic test suite runs without external dependencies, the full test suite may require mocking of:

- `tweepy` (Twitter API library)
- `vaderSentiment` (Sentiment analysis)
- `language_check` (Grammar checking)
- `nltk` (Natural language processing)

The test suite uses extensive mocking to avoid requiring actual installations of these dependencies.

## Design Principles

The test suite follows these principles:

1. **Minimal Code Changes**: Tests are additive and don't modify existing code
2. **Comprehensive Mocking**: External APIs and services are fully mocked
3. **Real-World Data**: Sample tweets use authentic language patterns
4. **Dialect Awareness**: UK/US English differences are explicitly tested
5. **Error Resilience**: Tests verify graceful handling of edge cases