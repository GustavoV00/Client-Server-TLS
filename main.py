# Trabalho para a disciplina Tópicos em Redes 
# Sistema cliente/servidor com comunicação segura
# Autores: Gustavo Valente Nunes | GRR: 20182557 
#          Henrique Prokopenko | GRR20186712
# Data: 31/05/2023

from utils import log
from utils import utils as cf
from client_server.client import client
from client_server.server import server
from scapy.all import *

import time
import sys
import logging

config_path = "config.ini"


# Função de configuração, que indica o que fazer com os pacotes sniffados
def sniffTcpPacket(pkt):
    # Verifica se existe o TCP no pacote 
    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        # Caso exista, apenas imprime a porta da origem e destino e imprime o payload
        print("TCP port: {} --> {} && TCP Payload: {} \n".format(tcp.sport, tcp.dport, tcp.payload))
        if Raw in pkt:
            load = pkt[Raw].load
            print(load)

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
                client.close_communication()
                break
            except ConnectionRefusedError:
                logger.info("Servidor não está respondendo, tentando novamente em 5 segundos...")
                time.sleep(5)

    if sys.argv[1] == "--clientintruder":
        logger = log.Logging.get_logger("Client")
        parser = cf.create_parser(config_path)

        while True:
            try:
                client = client.Client(parser.config["intruder"])
                client.start_communication_with_server()
                client.close_communication()
                break
            except ConnectionRefusedError:
                logger.info("Servidor não está respondendo, tentando novamente em 5 segundos...")
                time.sleep(5)
     
    elif sys.argv[1] == "--serverintruder":
        logger = log.Logging.get_logger("Server")

        logger.info("Gerando dados no servidor!")
        hash_table = cf.generate_db_values()
        logger.info("Dados gerados com sucesso")

        logger.info("Configurando o parser de configuração!")
        parser = cf.create_parser(config_path)
        logger.info("Terminado a configuração do parser do servidor!")

        server = server.Server(hash_table, parser.config["intruder"])
        server.start_communication_with_client()
        server.close_communication()

    elif sys.argv[1] == "--server":
        logger = log.Logging.get_logger("Server")

        logger.info("Gerando dados no servidor!")
        hash_table = cf.generate_db_values()
        logger.info("Dados gerados com sucesso")

        logger.info("Configurando o parser de configuração!")
        parser = cf.create_parser(config_path)
        logger.info("Terminado a configuração do parser do servidor!")

        server = server.Server(hash_table, parser.config["server"])
        server.start_communication_with_client()
        server.close_communication()


    elif sys.argv[1] == "--sniffer":
        # Função do scapy para fazer o sniffer
        # sniff(iface="lo", filter='tcp', prn=sniffTcpPacket)
        sniff(iface="lo", filter='dst port 5002', prn=sniffTcpPacket)




