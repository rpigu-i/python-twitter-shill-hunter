import argparse
from input import ProcessInputYaml
from gen_logo import Logo
from twitter_shill_hunter import TwitterShillHunter

def main():
    """
    Function to kick off the show.
    """

    logo = Logo()
    logo.generate_logo()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "yaml",
        help=" a YAML configuration file")
    args = parser.parse_args()
    process_input(args.yaml)


def process_input(yaml_file):
    """
    Create a new YAML parsing object
    and dump the content out as a dict
    """
    print "Processing input YAML"
    yaml_to_dict = ProcessInputYaml()
    yaml_to_dict = yaml_to_dict.yaml_processor(yaml_file)
    shill_hunter = TwitterShillHunter(yaml_to_dict)    


if __name__ == "__main__":
    main()
