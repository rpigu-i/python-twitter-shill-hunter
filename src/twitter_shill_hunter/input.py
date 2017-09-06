import yaml


class ProcessInputYaml():
    """
    Class to take an input YAML file
    of config. Opens it and returns it
    for processing
    """

    def yaml_processor(self, yamldoc):
        """
        Open the YAML doc and return to
        caller
        """
        config = {}
        opendoc = open(yamldoc, "r")
        config = yaml.load(opendoc)
        return config
