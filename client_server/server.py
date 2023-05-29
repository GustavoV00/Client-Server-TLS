from utils import log
from dotenv import dotenv_values

import socket
import ssl
import json


class Server(object):
    """
    Class that handle with server communication
    """

    def __init__(self, hash_table, parser):
        self.logger = log.Logging.get_logger(self.__class__.__name__)
        self.server_config = parser
        self.host = self.server_config["hostname"]
        self.port = int(self.server_config["port"])
        self.env_variables = dotenv_values(self.server_config["env"])

        self.hash_table = hash_table
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

        ssl_context.load_verify_locations(self.server_config["cert"])
        ssl_context.load_cert_chain(certfile=self.server_config["cert"], keyfile=self.server_config["key"])
        

        # SSL handshake
        secure_client_socket = ssl_context.wrap_socket(client, server_side=True)
        self.logger.info("Conexão estabelecida com sucesso!")
        
        while True:
            
            self.logger.info("Lendo mensagem do cliente")
            msg_from_client = secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()

            # Msg should be the CRUD
            result_data, msg_translated = self.crud_handler(msg_from_client)
            self.logger.info(f"Mensagem recebida de {address} -> {msg_translated}")

            if(result_data != 0):
                self.logger.info("Respondendo o cliente!")
                secure_client_socket.send(result_data.encode())

            if result_data == 0:
                self.logger.info(f"Finalizando comunicação com o cliente: {self.host}:{self.port}")
                secure_client_socket.close()
                return 

    def close_communication(self):
        self.socket_servidor.close()


    # PRECISA FAZER UM CRUD DESSE PARA O CLIENT
    def crud_handler(self, msg):
        return self.switch(msg)

    def switch(self, msg):
        msg = int(msg)
        if(msg == int(self.env_variables["GET_ALL"])):
            return self.get_all()
        
        elif(msg == int(self.env_variables["GET_BY_ID"])):
            self.get_by_id()

        elif(msg == int(self.env_variables["CREATE"])):
            self.create()

        elif(msg == int(self.env_variables["UPDATE_ALL"])):
            pass
        elif(msg == int(self.env_variables["UPDATE_BY_ID"])):
            pass
        elif(msg == int(self.env_variables["DELETE_ALL"])):
            pass
        elif(msg == int(self.env_variables["DELETE_BY_ID"])):
            pass
        elif(msg == 0):
            return [0, "Fechando Conexão!"]

    def get_all(self):
            return [json.dumps(self.hash_table.table), "Consultar todos os dados!"]

    def get_by_id(self, id):
        pass

    def create(self):
        pass

    def update_all():
        pass

    def update_by_id():
        pass

    def delete_all():
        pass

    def delete_by_id():
        pass