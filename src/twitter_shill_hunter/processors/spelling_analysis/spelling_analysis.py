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
        
        scanner = language_check.LanguageTool(dialect)

        print("Chosen language/dialect: " + str(dialect))

        for tweet in tweets_and_date:
            # Get words from tweet text
            words = tweet['text'].lower().split()
            # Find words that may be misspelled
            misspelled = spell.unknown(words)
             

            for i,k in enumerate(matches):
                print("----------------")
                print("Context: ") 
                print(matches[i].context.encode('ascii'))
                print("Rule Id:" + str(matches[i].ruleId))
                print("Category: " + matches[i].category)
                print("Based upon language/grammar user may have meant: ")
                did_you_mean = ""
                if matches[i].replacements:
                    for m in matches[i].replacements:
                        did_you_mean = did_you_mean + m.encode('ascii', 'ignore').decode('ascii') + ' ,'
                print(did_you_mean)


