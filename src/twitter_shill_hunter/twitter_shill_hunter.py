import pkg_resources
import json
import inspect
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from .tweet_text_extractor import TweetTextExtractor 

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
        Create Oauth 
        """

        self.oauth = OAuth(self.access_token, self.access_secret, 
                          self.consumer_key, self.consumer_secret)
 

    def initiate_api(self):
        """
        Initiate twitter REST API
        and grab list of targets tweets. 
        """
        try: 
            twitter = Twitter(auth=self.oauth) 
            get_tweets = twitter.statuses.user_timeline(screen_name=self.target, exclude_replies=True)
            tweet_extractor = TweetTextExtractor(get_tweets)
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

            params_to_pass = inspect.getfullargspec(self.loaded_processor_plugin_dict[p]().process_data)

            dynamic_args.append(tweets_and_time)
            for f in params_to_pass.args:
                if f != 'tweets_and_date' and f != 'self': 
                    dynamic_args.append(eval('self.'+f))

               
            self.call_processor(p, dynamic_args)

    def call_processor(self, p, args):
            self.loaded_processor_plugin_dict[p]().process_data(*args)
        

  
