from utils import log
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
        print("4 - Atualizar todos")
        print("5 - Atualizar por id")
        print("6 - Deletar todos")
        print("7 - Deletar por id")
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

                if(option.isdigit()):
                    option = int(option)
                    if(option <= 7 and option >= 0):
                        valid_input = True
                        if(option == 0):
                            sair = True
                    else:
                        self.logger.info("Input de usuário está fora das opções corretas!")
                else:
                    self.logger.info("Input de usuário não é um número, tente novamente!")

            if(option > 0):
                self.logger.info(f"Enviando mensagem para o servidor: {option}")
                self.send_message(str(option))
                resposta = self.secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
                self.logger.info(f"Resposta recebida do servidor: {resposta}")


    def close_communication(self):
        self.logger.info("Enviando mensagem - 'Sair' - para terminar a comunicação!")
        self.send_message(self.env_variables["FINISH"])
        # self.logger.info(f"Resposta recebida do servidor: {resposta}")

        self.socket_cliente.close()
        self.secure_client_socket.close()
        self.logger.info("Client Finalizado!")