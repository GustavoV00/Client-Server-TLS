# Trabalho para a disciplina Tópicos em Redes 
# Sistema cliente/servidor com comunicação segura
# Autores: Gustavo Valente Nunes | GRR: 20182557 
#          Henrique Prokopenko | GRR20186712
# Data: 31/05/2023

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
    while(i < 30):
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

def print_server_options():
    print("---------OPÇÕES---------")
    print("0 - Sair")
    print("1 - Consultar")
    print("2 - Consultar por id")
    print("3 - Criar")
    print("4 - Atualizar por id")
    print("5 - Deletar todos")
    print("6 - Deletar por id")
    print("-----------------------")

def parse_str_to_int(string):
    return int(string)

def parse_int_to_str(integer):
    return str(integer)

def send_message(msg, logger, connection):
    logger.info("Encoding a mensagem!")
    connection.send(msg.encode())

def recv_message(logger, connection, msg_size):
    logger.info("Recebendo mensagem do servidor!")

    return connection.recv(msg_size).decode()