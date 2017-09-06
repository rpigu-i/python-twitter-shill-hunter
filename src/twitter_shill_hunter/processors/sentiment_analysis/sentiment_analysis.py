from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalysis():
    """
    Class to dervice sentiment
    from tweets based upon a 
    list of provided keywords
    """

    def process_data(self, tweets_and_date, search_terms):
        """
        Data processing function
        """

        sia = SentimentIntensityAnalyzer()

        for tweet in tweets_and_date:
            words_found = []
            for st in search_terms:
                if st in tweet['text']:
                    words_found.append(st) 

            if len(words_found) > 0:

                print "The following search terms were found:"

                for w in words_found:
                    print w

                print tweet['date']
                print tweet['text']  
                sps = sia.polarity_scores(tweet['text'])
                for k in sps:
                    print "%s value is: %s" % (k,sps[k])
                print "-------------------------"

            else:
                print "No search terms found in tweet on:"
                print tweet['date'] 
                print "-------------------------"          

