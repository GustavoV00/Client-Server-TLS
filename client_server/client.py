from utils import log
import socket
import ssl


class Client(object):
    def __init__(self, host, port):
        self.logger = log.Logging.get_logger(self.__class__.__name__)
        self.host = host
        self.porta = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect(('localhost', self.porta))

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_verify_locations("cert_client/certificado.crt")

        # SSL handshake
        self.secure_client_socket = ssl_context.wrap_socket(self.socket_cliente, server_hostname="localhost")



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
        sair = ""
        while True and sair != "Y":
            self.logger.info("Lendo a entrada do usuário!")
            msg = input("Cliente: ")

            self.logger.info(f"Enviando mensagem para o servidor: {msg}")
            self.send_message(msg)
            resposta = self.secure_client_socket.recv(1024).decode()
            self.logger.info(f"Resposta recebida do servidor: {resposta}")

            sair = input("Deseja parar a comunicação? Y/n: ")

    def close_communication(self):
        self.logger.info("Enviando mensagem para terminar a comunicação!")
        self.send_message("terminar")
        # self.logger.info(f"Resposta recebida do servidor: {resposta}")

        self.socket_cliente.close()
        self.secure_client_socket.close()
