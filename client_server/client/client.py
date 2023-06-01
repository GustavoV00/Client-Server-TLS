# Trabalho para a disciplina Tópicos em Redes 
# Sistema cliente/servidor com comunicação segura
# Autores: Gustavo Valente Nunes | GRR: 20182557 
#          Henrique Prokopenko | GRR20186712
# Data: 31/05/2023

from utils import log
from utils import utils
from utils import commands
from utils import utils as cf
from client_server.client import client_service

import socket
import ssl

class Client(object):
    def __init__(self, parser):
        self.logger = log.Logging.get_logger(self.__class__.__name__)
        self.logger.set
        self.commands = commands.Commands
        self.context = self.create_sll_context(parser)

        try:
            self.connection = self.create_socket_connection(parser)
            self.logger.info("Conexão estabelecida com sucesso!")
        except Exception as e:
            self.logger.info(f"Erro ao criar conexão com o servidor: {e}")
            exit(1)

        self.client_service = client_service.ClientService(self.logger, self.connection, self.commands.SIZE.value)

    def create_sll_context(self, parser):
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(parser["server_cert"]) # Passa o certificado do servidor como confiável
        context.load_cert_chain(parser["cert"], parser["key"])
        return context

    def create_socket_connection(self, parser):
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SSL handshake
        secure_client_socket = self.context.wrap_socket(socket_client, server_hostname=parser["hostname"], server_side=False)
        secure_client_socket.connect((parser["hostname"], int(parser["port"])))
        return secure_client_socket

    def start_communication_with_server(self):
        sair = False
        option = ""
        while not sair:
            self.logger.info("Imprimindo opções disponíveis!")
            valid_input = False
            while not valid_input:
                utils.print_server_options()
                option = input("Digite a opção que deseja(apenas o número): ")

                if(utils.validate_number_in_range(option, 0, 7, self.logger)):
                    if(int(option) == 0):
                        valid_input = True
                        sair = True
                    self.send_response_handler(option)

    def send_response_handler(self, option):
        option = int(option)
        if(option == self.commands.GET_ALL.value):
            self.logger.info("Enviando mensagem para o servidor: Consultar!")
            self.client_service.get_all(str(option))

        if(option == self.commands.GET_BY_ID.value):
            self.logger.info("Enviando mensagem para o servidor: Consultar por id!")
            self.client_service.get_by_id(str(option))

        if(option == self.commands.CREATE.value):
            self.logger.info("Enviando mensagem para o servidor: Criar!")
            self.client_service.create(str(option))

        if(option == self.commands.UPDATE_BY_ID.value):
            self.logger.info("Enviando mensagem para o servidor: Atualizar por id!")
            self.client_service.update_by_id(str(option))

        if(option == self.commands.DELETE_ALL.value):
            self.logger.info("Enviando mensagem para o servidor: Deletar todos")
            self.client_service.delete_all(str(option))

        if(option == self.commands.DELETE_BY_ID.value):
            self.logger.info("Enviando mensagem para o servidor: Deletar por id")
            self.client_service.delete_by_id(str(option))

        elif(option == self.commands.FINISH.value):
            self.logger.info("Enviando mensagem para o servidor: Sair!")
            self.client_service.finish(str(option))

    def close_communication(self):
        # self.logger.info(f"Resposta recebida do servidor: {resposta}")

        self.connection.close()
        self.logger.info("Client Finalizado!")