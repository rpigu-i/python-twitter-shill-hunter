
class GeoAnalysis():
    """
    Class to derive geo data
    from tweets
    """

    def process_data(self, tweets_and_date):
        """
        Data processing function
        """

        for tweet in tweets_and_date:
            print tweet['created_at']
            print tweet['coordinates']
            print tweet['source']
