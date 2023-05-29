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
            
            self.logger.info("Recebendo opção do cliente!")
            msg_from_client = secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()

            # Msg should be the CRUD
            if(not self.send_response_handler(msg_from_client, secure_client_socket, address)):
                return

    # PRECISA FAZER UM CRUD DESSE PARA O CLIENT
    def send_response_handler(self, msg, secure_client_socket, address):
        return self.switch(msg, secure_client_socket, address)

    def switch(self, msg, secure_client_socket, address):
        self.logger.info("Respondendo o cliente!")
        if(msg == self.env_variables["GET_ALL"]):
            msg_translated = "Consultar todos os dados!"
            return self.get_all(msg_translated, secure_client_socket, address)
        
        elif(msg == self.env_variables["GET_BY_ID"]):
            msg_translated = "Consultar dado por id!"
            return self.get_by_id(msg_translated, secure_client_socket, address)

        elif(msg == self.env_variables["CREATE"]):
            msg_translated = "Criar um novo dado!"
            return self.create(msg_translated, secure_client_socket, address)

        elif(msg == self.env_variables["UPDATE_BY_ID"]):
            msg_translated = "Atualizar um dado por id!"
            return self.update_by_id(msg_translated, secure_client_socket, address)
        # elif(msg == self.env_variables["DELETE_ALL"]):
        #     pass
        # elif(msg == self.env_variables["DELETE_BY_ID"]):
        #     pass
        elif(msg == self.env_variables["FINISH"]):
            msg_translated = "Fechando Conexão!"
            return self.finish(msg_translated, secure_client_socket, address)

    def get_all(self, msg, secure_client_socket, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")
        self.logger.info("Lendo usuarios do Banco de Dados")
        result_data = json.dumps(self.hash_table.table)
        self.logger.info("Enviando esses usuários para o cliente!")
        secure_client_socket.send(result_data.encode())
        return True

    def get_by_id(self, msg, secure_client_socket, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")

        self.logger.info("Enviando mensagem requisitando um id ao cliente!")
        result_data = "'Digite o id que deseja!'"
        secure_client_socket.send(result_data.encode())

        data_id = secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Recebendo do cliente o novo id: '{data_id}")

        self.logger.info("Procurando elemento no banco de dados")
        result = self.hash_table.get(int(data_id))

        if(result != None):
            self.logger.info("Enviando dado encontrado no banco de dados")
            secure_client_socket.send(result.encode())
        else:
            self.logger.info("Usuario com id: '{data_id}' não encontrado!")
            result = "Usuário não encontrado! Tente outro!"
            secure_client_socket.send(result.encode())
        return True

    def create(self, msg, secure_client_socket, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")

        self.logger.info("Enviando mensagem requisitando ao cliente o nome do novo usuário!")
        result_data = "'Digite o nome do novo usuario'"
        secure_client_socket.send(result_data.encode())

        usuario = secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Nome do novo usuário recebido: '{usuario}'")
        self.hash_table.insert(usuario)

        self.logger.info("Usuario inserido no banco com sucesso!")
        self.logger.info("Enviando mensagem de confirmação para o cliente!")
        result_data = f"'Usuario '{usuario}' criado com sucesso'"
        secure_client_socket.send(result_data.encode())
        return True

    def update_by_id(self, msg, secure_client_socket, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")
        self.logger.info("Enviando mensagem requisitando ao cliente o id do dado que deseja atualizar!")

        result_data = "'Digite o nome do novo id'"
        secure_client_socket.send(result_data.encode())

        data_id = secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
        self.logger.info(f"Recebendo do cliente o novo id: '{data_id}")

        self.logger.info("Procurando elemento no banco de dados")
        result = self.hash_table.get(int(data_id))

        if(result != None):
            self.logger.info("Enviando mensagem requisitando o nome desse novo dado!")
            result = "'Digite o nome do novo usuario'"
            secure_client_socket.send(result.encode())

            new_username = secure_client_socket.recv(int(self.env_variables["SIZE"])).decode()
            self.logger.info(f"Recebendo o novo nome: '{new_username}' do id: '{data_id}")

            self.hash_table.update(int(data_id), new_username)
            self.logger.info("Dado atualizado com sucesso!")

            result_data = "'Dado atualizado com sucesso!'"
            secure_client_socket.send(result_data.encode())
        else:
            self.logger.info("Usuario com id: '{data_id}' não encontrado!")
            result = "Usuário não encontrado! Tente outro!"
            secure_client_socket.send(result.encode())
        return True

    def delete_all():
        pass

    def delete_by_id():
        pass

    def finish(self, msg, secure_client_socket, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")
        self.logger.info(f"Finalizando comunicação com o cliente: {self.host}:{self.port}")
        self.close_communication()
        secure_client_socket.close()
        return False

    # TO DO: Close secure_client_socket and socket_servidor at the same method
    def close_communication(self):
        self.socket_servidor.close()