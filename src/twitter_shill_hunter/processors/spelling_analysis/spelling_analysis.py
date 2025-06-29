import sys
import language_tool_python

# Note: This module uses the 'language-tool-python' package for real grammar and 
# spelling analysis, replacing the previous stub implementation.

class SpellingAnalysis():
    """
    Class to highlight
    spelling issues 
    """
    
    def process_data(self, tweets_and_date, dialect):
        """
        Data processing function
        """

        scanner = language_tool_python.LanguageTool(dialect)
        print("Chosen language/dialect: " + str(dialect))

        try:
            for tweet in tweets_and_date:
                # Handle Unicode text properly for Python 3
                tweet_text = tweet['text']
                if isinstance(tweet_text, str):
                    # Remove non-ASCII characters safely
                    tweet_text = ''.join(char for char in tweet_text if ord(char) < 128)
                
                matches = scanner.check(tweet_text)
                 
                for i,k in enumerate(matches):
                    print("----------------")
                    print("Context: ") 
                    # Handle context encoding safely
                    context = matches[i].context
                    if isinstance(context, str):
                        context = ''.join(char for char in context if ord(char) < 128)
                    print(context)

                    print("Rule Id:" + str(matches[i].ruleId))
                    print("Category: " + matches[i].category)
                    print("Based upon language/grammar user may have meant: ")
                    did_you_mean = ""
                    if matches[i].replacements:
                        for m in matches[i].replacements:

                            # Handle replacement text safely
                            replacement = m
                            if isinstance(replacement, str):
                                replacement = ''.join(char for char in replacement if ord(char) < 128)
                            did_you_mean = did_you_mean + replacement + ' ,'
                    print(did_you_mean)
        finally:
            # Always close the LanguageTool instance to clean up resources
            scanner.close()

