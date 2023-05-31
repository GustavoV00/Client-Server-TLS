# Trabalho para a disciplina Tópicos em Redes 
# Sistema cliente/servidor com comunicação segura
# Autores: Gustavo Valente Nunes | GRR: 20182557 
#          Henrique Prokopenko | GRR20186712
# Data: 31/05/2023

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
