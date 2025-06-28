import pkg_resources
import os 
from ...input import ProcessInputYaml

 
class GrammarAnalysis():
    """
    Class to derive target
    grammar from tweets
    """

    dialect = ""
    valid_dialects = []

    def process_data(self, tweets_and_date, dialect):
        """
        Data processing function
        """
        self.dialect = str(dialect) 
        self.tweets_and_date = tweets_and_date
     
        print("Chosen language/dialect: " + self.dialect)
        self.get_lang_dialects()
        self.analyze_dialect()

    def get_lang_dialects(self):
        """
        Get a list of dialects associated 
        with the language.
        """
        language = self.dialect.split('-')[0]
 
        resource_path = '/dialect_mappings/'+str(language)
        resource_path = pkg_resources.resource_filename(__name__, resource_path)
        for file in os.listdir(resource_path):
            if file.endswith(".yaml") and file != self.dialect+".yaml":
                self.valid_dialects.append('/'.join((resource_path,file)))

         

    def analyze_dialect(self):
        """
        Review the tweets 
        to see if spellings
        match dialect
        """

        for dialect in self.valid_dialects:
            dialect_words = self.process_input(dialect)

            for tweet in self.tweets_and_date:
                for word in dialect_words['words']:
                    if word in tweet['text']:
                        print("Dialect is: " + str(dialect.split('/')[-1]))
                        print("Word found is: " + word)
                


    def process_input(self, yaml_file):
        """
        Create a new YAML parsing object
        and dump the content out as a dict
        """
        yaml_to_dict = ProcessInputYaml()
        yaml_to_dict = yaml_to_dict.yaml_processor(yaml_file)
        return yaml_to_dict
