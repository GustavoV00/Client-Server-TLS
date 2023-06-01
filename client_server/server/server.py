# Trabalho para a disciplina Tópicos em Redes 
# Sistema cliente/servidor com comunicação segura
# Autores: Gustavo Valente Nunes | GRR: 20182557 
#          Henrique Prokopenko | GRR20186712
# Data: 31/05/2023

from utils import log
from utils import commands
from client_server.server import server_service

import socket
import ssl


class Server(object):
    def __init__(self, hash_table, parser):
        self.logger = log.Logging.get_logger(self.__class__.__name__)
        self.data = hash_table
        self.commands = commands.Commands
        self.ssl_context = self.create_sll_context(parser)
        self.server_socket = self.create_socket(parser)
        self.server_service = server_service.ServerService(self.logger, self.data, self.commands)
        self.connection = None

    def create_sll_context(self, parser):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_verify_locations(parser["client_cert"]) # Certicado confiavel pelo servidor
        ssl_context.load_cert_chain(certfile=parser["cert"], keyfile=parser["key"])

        return ssl_context

    def create_socket(self, parser):
        self.logger.info("Iniciando servidor!")
        host = parser["hostname"]
        port = int(parser["port"])

        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.bind((host, port))
        skt.listen(5)

        self.logger.info(f"Servidor iniciado: {host}:{port}")

        return skt


    def start_communication_with_client(self):
        
        client, address = self.server_socket.accept()
        self.connection = self.ssl_context.wrap_socket(client, server_side=True) # ssl handshake
        self.logger.info("Conexão estabelecida com sucesso!")
        
        while True:
            
            self.logger.info("Recebendo opção do cliente!")
            msg_from_client = self.connection.recv(self.commands.SIZE.value).decode()

            # Msg should be the CRUD
            if(not self.send_response_handler(msg_from_client, self.connection, address)):
                return

    # PRECISA FAZER UM CRUD DESSE PARA O CLIENT
    def send_response_handler(self, msg, secure_client_socket, address):
        self.logger.info("Respondendo o cliente!")
        msg = int(msg)
        if(msg == self.commands.GET_ALL.value):
            msg_translated = "Consultar todos os dados!"
            return self.server_service.get_all(msg_translated, secure_client_socket, address)
        
        elif(msg == self.commands.GET_BY_ID.value):
            msg_translated = "Consultar dado por id!"
            return self.server_service.get_by_id(msg_translated, secure_client_socket, address)

        elif(msg == self.commands.CREATE.value):
            msg_translated = "Criar um novo dado!"
            return self.server_service.create(msg_translated, secure_client_socket, address)

        elif(msg == self.commands.UPDATE_BY_ID.value):
            msg_translated = "Atualizar um dado por id!"
            return self.server_service.update_by_id(msg_translated, secure_client_socket, address)

        elif(msg == self.commands.DELETE_ALL.value):
            msg_translated = "Deletar todos os dados!"
            return self.server_service.delete_all(msg_translated, secure_client_socket, address)

        elif(msg == self.commands.DELETE_BY_ID.value):
            msg_translated = "Deletar dado por id!"
            return self.server_service.delete_by_id(msg_translated, secure_client_socket, address)

        elif(msg == self.commands.FINISH.value):
            msg_translated = "Fechando Conexão!"
            return self.server_service.finish(msg_translated, address)

    def close_communication(self):
        self.connection.close()
        self.server_socket.close()