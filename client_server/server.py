from utils import log
import socket


class Server(object):
    """
    Class that handle with server communication
    """

    def __init__(self, host, port):
        self.logger = log.Logging.get_logger(self.__class__.__name__)
        self.host = host
        self.port = port
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        self.logger.info("Iniciando servidor!")
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen(1)
        self.logger.info(f"Servidor iniciado: {self.host}:{self.port}")

    def send_message_to_client(self, msg):
        self.socket_servidor.send(msg)

    def start_communication_with_client(self):
        while True:
            client, address = self.socket_servidor.accept()
            self.logger.info("Conexão estabelecida com sucesso!")
            self.logger.info("Lendo mensagem do cliente")
            msg = client.recv(1024).decode("utf-8")
            self.logger.info(f"Mensagem recebida de {address}:{msg}")

            self.logger.info("Respondendo o servidor!")
            res = "Ok"
            self.send_message_to_client(res)

            if msg == "terminar":
                self.logger.info(
                    f"Finalizando comunicação com o cliente: {self.host}:{self.port}"
                )
                break

    def close_communication(self):
        self.socket_servidor.close()
