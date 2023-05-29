class StartConfig:
    """
        This class that represents the 'configurations.ini' file, 
        under the configs/
    """

    def __init__(self, config):
        self.config = config

    def read_config(self, path_to_config):
        """
            Read the configurations.ini file
        """
        self.config.read(path_to_config)
