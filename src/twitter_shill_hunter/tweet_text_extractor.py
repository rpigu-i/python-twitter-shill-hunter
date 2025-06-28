

class TweetTextExtractor():

    tweet_json = {}
    processed_tweets = []

    def __init__(self, tweet_json):
        """
        Grab the input
        JSON object for
        processing
        """

        self.tweet_json = tweet_json


    def extract_text(self):
        """
        Extract text content
        from tweets ready for
        processing.
        """
        
        for i in self.tweet_json:
            tweet_data = {}
            tweet_data['date'] = i['created_at']
            # Handle both 'text' and 'full_text' fields for compatibility
            tweet_data['text'] = i.get('full_text', i.get('text', ''))
            tweet_data['coordinates'] = i['coordinates']
            tweet_data['place'] = i['place']
            tweet_data['source'] = i['source']
            tweet_data['created_at'] = i['created_at']
            self.processed_tweets.append(tweet_data)

        return self.processed_tweets

            
  
     
