from utils import log
from utils import utils
from dotenv import dotenv_values

import socket
import ssl


class Client(object):
    def __init__(self, parser):
        self.logger = log.Logging.get_logger(self.__class__.__name__)
        self.client_config = parser

        self.host = self.client_config["hostname"]
        self.porta = int(self.client_config["port"])

        self.env_variables = dotenv_values(self.client_config["env"])

        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect((self.client_config["hostname"], self.porta))

        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

        # ssl_context.verify_mode = ssl.CERT_REQUIRED

        self.ssl_context.load_verify_locations(self.client_config["cert"])

        # SSL handshake
        self.secure_client_socket = self.ssl_context.wrap_socket(self.socket_cliente, server_hostname=self.client_config["hostname"])

    def print_server_options(self):
        print("---------OPÇÕES---------")
        print("0 - Sair")
        print("1 - Consultar")
        print("2 - Consultar por id")
        print("3 - Criar")
        print("4 - Atualizar por id")
        print("5 - Deletar todos")
        print("6 - Deletar por id")
        print("-----------------------")

    def send_message(self, msg):
        """
        Args:
            msg (str): message to be sent

        Returns:
            str: decoded message from server
        """
        self.logger.info("Encoding a mensagem!")
        self.secure_client_socket.send(msg.encode())

    def start_communication_with_server(self):
        sair = False
        option = ""
        while not sair:
            self.logger.info("Imprimindo opções disponíveis!")
            valid_input = False
            while not valid_input:
                self.print_server_options()
                option = input("Digite a opção que deseja(apenas o número): ")

                if(utils.validate_number_in_range(option, 0, 7, self.logger)):
                    if(int(option) == 0):
                        valid_input = True
                        sair = True
                    self.logger.info(f"Enviando mensagem para o servidor: {option}!")
                    self.send_response_handler(option)

    def send_response_handler(self, option):
        self.switch(option)

    def switch(self, option):
        option = str(option)
        if(option == self.env_variables["GET_ALL"]):
            self.get_all(option)

        if(option == self.env_variables["GET_BY_ID"]):
            self.get_by_id(option)

        if(option == self.env_variables["CREATE"]):
            self.create(option)

        if(option == self.env_variables["UPDATE_BY_ID"]):
            self.update_by_id(option)

        elif(option == self.env_variables["FINISH"]):
            self.finish(option)

    def get_all(self, option):
        self.logger.info("Enviando mensagem para 'Consultar todos os dados'!")
        self.send_message(option)
        resposta = self.secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

    def get_by_id(self, option):
        self.logger.info("Enviando mensagem para 'Consultar dado por id'!")
        self.send_message(option)

        resposta = self.secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

        data_id = input("Digite o id: ")
        self.send_message(data_id)

        resposta = self.secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

    def create(self, option):
        self.logger.info("Enviando mensagem para 'Criar um novo dado'!")
        self.send_message(option)

        resposta = self.secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

        user = input("Digite o novo usuario: ")
        self.send_message(user)

        resposta = self.secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

    def update_by_id(self, option):
        self.logger.info("Enviando mensagem para 'Atualizar um dado'!")
        self.send_message(option)

        resposta = self.secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

        user = input("Digite o id: ")
        self.send_message(user)

        resposta = self.secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

        user = input("Digite o nome do usuario para atualizar: ")
        self.send_message(user)

        resposta = self.secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

    def finish(self, option):
        self.logger.info("Finalizando a comunicação com o servidor!")
        self.send_message(option)
        self.close_communication()

    def close_communication(self):
        # self.logger.info(f"Resposta recebida do servidor: {resposta}")

        self.socket_cliente.close()
        self.secure_client_socket.close()
        self.logger.info("Client Finalizado!")