from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalysis():
    """
    Class to derive sentiment
    from tweets based upon a 
    list of provided keywords
    """
    
    def __init__(self):
        self.aggregated_results = []


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

                result = {}
                search_terms_found = []

                print("The following search terms were found:")

                for w in words_found:
                     print(w)
                     search_terms_found.append(w)


                print(tweet['date'])
                print(tweet['text']) 
                
                result['date'] =  tweet['date']
                result['tweet'] = tweet['text']
                result['search_terms'] = search_terms_found 
                  
                sps = sia.polarity_scores(tweet['text'])
                for k in sps:
                    print("%s value is: %s" % (k,sps[k]))
                    result[k] = sps[k]
                
                print("-------------------------")
                self.aggregated_results.append(result)
            else:
                print("No search terms found in tweet on:")

                print(tweet['date'])

                print("-------------------------")          

        self.aggregate_search_results(search_terms)


    def aggregate_search_results(self, search_terms):
        """
        Aggregate the search results 
        and sentiment associated with them.
        """
        combined_results = {}
        compound_result = {}
        total_compound_val = 0
        total_count = 0

        for st in search_terms:
            counter = 0 
            compound_result[st] = 0
            for r in self.aggregated_results:
                for w in r['search_terms']:
                    if w == st:
                        compound_result[st] += r['compound']
                        counter += 1
                    
            if counter > 0:
                compound_result[st] = compound_result[st] / counter
                total_compound_val += compound_result[st]
                total_count += 1

        # Calculate overall average compound value
        agg_compound_val = total_compound_val / total_count if total_count > 0 else 0

        print("Aggregated average compound value for search terms")
        print(agg_compound_val)
        combined_results['tweets_analyzed'] = self.aggregated_results
        combined_results['compound_search_results'] = agg_compound_val 
        return compound_result 
         
 

         

