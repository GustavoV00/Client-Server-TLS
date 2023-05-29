import configparser
import random

from utils import start_config
from utils import hash_table


def create_parser(config_path):
    """
        this creates a parser for cert/cert.ini file
    """
    parser = start_config.StartConfig(configparser.ConfigParser())
    parser.read_config(config_path)
    return parser


def generate_db_values():

    i = 0
    hash = hash_table.HashTable()
    while(i < 100):
        usuario = f"usuario{random.randint(0, 1000)}"
        if(hash.insert(usuario)):
            i += 1
        else:
            i -= 1

    return hash

def validate_number_in_range(value, range1, range2, logger):
    if(value.isdigit()):
        value = int(value)
        if(value >= range1 and value <= range2):
            return True
        else:
            logger.info("Input de usuário está fora das opções corretas!")
    else:
        logger.info("Input de usuário não é um número, tente novamente!")

    return False
