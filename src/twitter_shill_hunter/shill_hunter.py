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
    search_terms = []
    dialect = ''

    def __init__(self, yaml_dict):
        """"
        Assign tokens and
        secrets needed by
        application
        """
        yaml_to_dict = yaml_dict["config"]
        self.access_token = yaml_to_dict['access_token']
        self.access_secret = yaml_to_dict['access_secret']
        self.consumer_key = yaml_to_dict['consumer_key']
        self.consumer_secret = yaml_to_dict['consumer_secret']
        self.target = yaml_to_dict['target']
        self.search_terms = yaml_to_dict['search_terms'] 
        self.dialect = yaml_to_dict['dialect']
        self.authenticate()
        self.initiate_api()


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
        try: 
            twitter = Twitter(auth=self.oauth) 
            twitter.statuses.user_timeline(screen_name=self.target)
        except Exception as e:
            print e 
  
