from utils import log
import socket
import ssl


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
        self.socket_servidor.bind(('localhost', self.port))
        self.socket_servidor.listen(1)
        self.logger.info(f"Servidor iniciado: {self.host}:{self.port}")


    def start_communication_with_client(self):
        
        client, address = self.socket_servidor.accept()

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_verify_locations("cert_client/certificado.crt")
        ssl_context.load_cert_chain(certfile="cert_server/certificado.crt", keyfile="cert_server/chave.key")
        

        # SSL handshake
        secure_client_socket = ssl_context.wrap_socket(client, server_side=True)
        self.logger.info("Conexão estabelecida com sucesso!")
        
        while True:
            
            self.logger.info("Lendo mensagem do cliente")
            msg = secure_client_socket.recv(1024).decode()
            self.logger.info(f"Mensagem recebida de {address}:{msg}")

            self.logger.info("Respondendo o cliente!")
            res = "Ok"
            secure_client_socket.send(res.encode())

            if msg == "terminar":
                self.logger.info(f"Finalizando comunicação com o cliente: {self.host}:{self.port}")
                secure_client_socket.close()
                break

    def close_communication(self):
        self.socket_servidor.close()
