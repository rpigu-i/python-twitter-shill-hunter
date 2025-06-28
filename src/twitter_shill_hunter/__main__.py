import argparse
from .input import ProcessInputYaml
from .gen_logo import Logo
from .twitter_shill_hunter import TwitterShillHunter

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
    parser.add_argument(
        "plugins",
        help="list of plugins to be used in output")

    args = parser.parse_args()
    plugins = plugin_processor('twitter_shill_hunter.processors', args.plugins)
    process_input(args.yaml, plugins)


def plugin_processor(cat, plugins):
    """
    Return a list of plugins
    to use
    """
    plugins_to_use = {}
    plugins_to_use[cat] = plugins.split(',')
    return plugins_to_use


def process_input(yaml_file, plugins):
    """
    Create a new YAML parsing object
    and dump the content out as a dict
    """
    print("Processing input YAML")
    yaml_to_dict = ProcessInputYaml()
    yaml_to_dict = yaml_to_dict.yaml_processor(yaml_file)
    shill_hunter = TwitterShillHunter(yaml_to_dict, plugins)


if __name__ == "__main__":
    main()
