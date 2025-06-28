import pkg_resources
import json
import inspect
import tweepy
from .tweet_text_extractor import TweetTextExtractor 

class TwitterShillHunter():
    """
    Class for analyzing a users
    historical posts on X (formerly Twitter)
    """

    access_token = ''
    access_secret = ''
    consumer_key = ''
    consumer_secret = ''
    target = ''
    api = None
    search_terms = []
    dialect = ''
    processors_plugin = 'twitter_shill_hunter.processors'
    loaded_processor_plugin_dict = {}

    def __init__(self, yaml_dict, plugins):
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
        self.loaded_processor_plugin_dict = self.load_plugins(
            self.processors_plugin,
            plugins)
 
        print("Processing target %s" % self.target)

        self.authenticate()
        self.initiate_api()
 

    def load_plugins(self, cat, plugins):
        """
        Load the plugin and store object in array
        """
        plugin_dict = {}
        for p in plugins[cat]:
            print("Loading plugin %s" % p)
            plugin_dict[p] = pkg_resources.load_entry_point(
                'twitter_shill_hunter', cat, p)
        return plugin_dict


    def authenticate(self):
        """
        Create X API authentication 
        """

        auth = tweepy.OAuth1UserHandler(
            self.consumer_key, self.consumer_secret,
            self.access_token, self.access_secret
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
 

    def initiate_api(self):
        """
        Initiate X API and grab list of target's posts.
        """
        try: 
            # Get user timeline using tweepy
            get_tweets = self.api.user_timeline(
                screen_name=self.target, 
                exclude_replies=True,
                include_rts=False,
                count=200,
                tweet_mode='extended'
            )
            
            # Convert tweepy Status objects to dict format expected by TweetTextExtractor
            tweets_json = []
            for tweet in get_tweets:
                tweets_json.append(tweet._json)
            
            tweet_extractor = TweetTextExtractor(tweets_json)
            tweets_and_time = tweet_extractor.extract_text()
            self.load_processors(tweets_and_time)
        except Exception as e:
            print(e) 

    def load_processors(self, tweets_and_time):
        """
        Load processors and pass
        list of tweets and their time
        stamps in
        """
 
        for p in self.loaded_processor_plugin_dict:
            dynamic_args = []
            params_to_pass = inspect.getargspec(self.loaded_processor_plugin_dict[p]().process_data)

            dynamic_args.append(tweets_and_time)
            for f in params_to_pass[0]:
                if f != 'tweets_and_date' and f != 'self': 
                    dynamic_args.append(eval('self.'+f))
               
            self.call_processor(p, dynamic_args)

    def call_processor(self, p, args):
            self.loaded_processor_plugin_dict[p]().process_data(*args)
        

  
