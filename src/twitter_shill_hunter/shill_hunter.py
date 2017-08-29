import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream


class TwitterShillHunter():
    """
    Class for analyzing a users
    historical tweets
    """

    access_token = ''
    access_secret = ''
    consumer_key = ''
    consumer_secret = ''
    target = ''
    oauth = '' 

    def __init__(self, acess_token, access_secret,
                 consumer_key, consumer_secret):
        """"
        Assign tokens and
        secrets needed by
        application
        """
     
        self.access_token = access_token
        self.access_secret = access_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.target = target
  

    def authenticate(self):
        """
        Create Oauth 
        """

        self.oauth = OAuth(self.access_token, self.access_secret, 
                          self.consumer_key, self.consumer_secret)
 

    def initiate_api(self):
        """
        Initiate twitter REST API
        """
     
        twitter = Twitter(auth=oauth) 
        twitter.statuses.user_timeline(screen_name=self.target)
  
