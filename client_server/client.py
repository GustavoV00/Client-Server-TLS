from utils import log
import socket


class Client(object):
    def __init__(self, host, port):
        self.logger = log.Logging.get_logger(self.__class__.__name__)
        self.host = host
        self.porta = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect((self.host, self.porta))

    def send_message(self, msg):
        """
        Args:
            msg (str): message to be sent

        Returns:
            str: decoded message from server
        """
        self.logger.info("Encoding a mensagem!")
        self.socket_cliente.send(msg.encode("utf-8"))
        return self.socket_cliente.recv(1024).decode("utf-8")

    def start_communication_with_server(self):
        sair = ""
        while True and sair != "Y":
            self.logger.info("Lendo a entrada do usuário!")
            msg = input("Cliente: ")

            self.logger.info(f"Enviando mensagem para o servidor: {msg}")
            self.send_message(msg)
            self.logger.info(f"Resposta recebida do servidor: {resposta}")

            sair = input("Deseja para a comunicação? Y/n")

    def close_communication(self):
        self.logger.info("Enviando mensagem para terminar a comunicação!")
        self.send_message("terminar")
        # self.logger.info(f"Resposta recebida do servidor: {resposta}")

        self.socket_cliente.close()
