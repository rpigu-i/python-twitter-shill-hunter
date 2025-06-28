import language_check

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
            matches = scanner.check(tweet['text'])
             
            for i,k in enumerate(matches):
                print("----------------")
                print("Context: ") 
                print(matches[i].context)
                print("Rule Id:" + str(matches[i].ruleId))
                print("Category: " + matches[i].category)
                print("Based upon language/grammar user may have meant: ")
                did_you_mean = ""
                if matches[i].replacements:
                    for m in matches[i].replacements:
                        did_you_mean = did_you_mean + str(m) + ' ,'
                print(did_you_mean)

