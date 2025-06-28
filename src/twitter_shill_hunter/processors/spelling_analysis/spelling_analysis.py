from spellchecker import SpellChecker

class SpellingAnalysis():
    """
    Class to highlight
    spelling issues 
    """
    
    def process_data(self, tweets_and_date, dialect):
        """
        Data processing function
        """
        

        spell = SpellChecker(language=dialect)

        print("Chosen language/dialect: " + str(dialect))

        for tweet in tweets_and_date:
            # Get words from tweet text
            words = tweet['text'].lower().split()
            # Find words that may be misspelled
            misspelled = spell.unknown(words)
             
            for word in misspelled:
                print("----------------")
                print("Context: " + tweet['text'])
                print("Misspelled word: " + word)
                print("Suggestions: ")
                suggestions = spell.candidates(word)
                if suggestions:
                    print(", ".join(list(suggestions)[:5]))  # Show top 5 suggestions
                else:
                    print("No suggestions available")


