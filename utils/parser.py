# Trabalho para a disciplina Tópicos em Redes 
# Sistema cliente/servidor com comunicação segura
# Autores: Gustavo Valente Nunes | GRR: 20182557 
#          Henrique Prokopenko | GRR20186712
# Data: 31/05/2023

import configparser
from utils import log

class Error(Exception):
    """
        Base error class of configparser class
    """

class ConfigParser(object):

    def __init__(self):
        self._logger = log.Logging.get_logger(self.__class__.__name__)

    def setup_config_parser(self, config_file):
        """
            Setup a config parser to a specific file
            :param config_file is a string type that points to configs/config_file
        """
        config = configparser.ConfigParser()
        config.read(config_file)

        return config

    def get_config_parser_section(self, config, section):
        """
            Get a specific section from config_file
            :param config is a configparser type 
            :param section is a string with the section name

        """

        try:
            docker_config = config[section]
        except Exception as err:
            print(f"Erro to find section! {err}")
            docker_config = False
            raise Error(f"Error to find section! {err}")

        return docker_config