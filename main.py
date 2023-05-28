from utils import log
from client_server import client
from client_server import server

import sys
import logging

localhost = "127.0.0.1"
port = 5000


if __name__ == "__main__":
    log.Logging.setup(True, None, logging.INFO)

    if len(sys.argv) < 2:
        print("Como rodar: python main.py --client ou python main.py --server")
        print(
            "Nota: Caso não tenha um servidor rodando, é preciso rodar primeiro o serivdor!"
        )
        sys.exit(1)

    if sys.argv[1] == "--client":
        client = client.Client(localhost, port)
        client.start_communication_with_server()
        client.close_communication()

    elif sys.argv[1] == "--server":
        server = server.Server(localhost, port)
        server.start_server()
        server.start_communication_with_client()
        server.close_communication()
