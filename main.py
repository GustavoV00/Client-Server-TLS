from utils import log
from utils import utils as cf
from client_server import client
from client_server import server

import time
import sys
import logging

localhost = "127.0.0.1"
config_path = "config.ini"


if __name__ == "__main__":
    log.Logging.setup(True, None, logging.INFO)

    if len(sys.argv) < 2:
        print("Como rodar: python main.py --client ou python main.py --server")
        print(
            "Nota: Caso não tenha um servidor rodando, é preciso rodar primeiro o cliente!"
        )
        sys.exit(1)

    if sys.argv[1] == "--client":
        logger = log.Logging.get_logger("Client")
        parser = cf.create_parser(config_path)

        while True:
            try:
                client = client.Client(parser.config["client"])
                client.start_communication_with_server()
                break
            except ConnectionRefusedError:
                logger.info("Servidor não está respondendo, tentando novamente em 5 segundos...")
                time.sleep(5)

    elif sys.argv[1] == "--server":
        logger = log.Logging.get_logger("Server")

        logger.info("Gerando dados no servidor!")
        hash_table = cf.generate_db_values()
        logger.info("Dados gerados com sucesso")

        logger.info("Configurando o parser de configuração!")
        parser = cf.create_parser(config_path)
        logger.info("Terminado a configuração do parser do servidor!")

        server = server.Server(hash_table, parser.config["server"])
        server.start_server()
        server.start_communication_with_client()

# TO DO: Do the kvs CRUD
# Fix the parser values in the correct palces
# Fix de TLS in the correct place using parser
# Finishing the TLS