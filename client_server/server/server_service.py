import json

class ServerService(object):
    def __init__(self, logger, data, commands):
        self.logger = logger
        self.data = data
        self.commands = commands


    def get_all(self, msg, secure_client_socket, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")
        self.logger.info("Lendo usuarios do Banco de Dados")
        result_data = json.dumps(self.data.table)
        self.logger.info("Enviando esses usuários para o cliente!")
        secure_client_socket.send(result_data.encode())
        return True

    def get_by_id(self, msg, secure_client_socket, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")

        self.logger.info("Enviando mensagem requisitando um id ao cliente!")
        result_data = "'Digite o id que deseja!'"
        secure_client_socket.send(result_data.encode())

        data_id = secure_client_socket.recv(self.commands.SIZE.value).decode()
        self.logger.info(f"Recebendo do cliente o novo id: '{data_id}")

        self.logger.info("Procurando elemento no banco de dados")
        result = self.data.get(int(data_id))

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

        usuario = secure_client_socket.recv(self.commands.SIZE.value).decode()
        self.logger.info(f"Nome do novo usuário recebido: '{usuario}'")
        self.data.insert(usuario)

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

        data_id = secure_client_socket.recv(self.commands.SIZE.value).decode()
        self.logger.info(f"Recebendo do cliente o novo id: '{data_id}")

        self.logger.info("Procurando elemento no banco de dados")
        result = self.data.get(int(data_id))

        if(result != None):
            self.logger.info("Enviando mensagem requisitando o nome desse novo dado!")
            result = "'Digite o nome do novo usuario'"
            secure_client_socket.send(result.encode())

            new_username = secure_client_socket.recv(self.commands.SIZE.value).decode()
            self.logger.info(f"Recebendo o novo nome: '{new_username}' do id: '{data_id}")

            self.data.update(int(data_id), new_username)
            self.logger.info("Dado atualizado com sucesso!")

            result_data = "'Dado atualizado com sucesso!'"
            secure_client_socket.send(result_data.encode())
        else:
            self.logger.info("Usuario com id: '{data_id}' não encontrado!")
            result = "Usuário não encontrado! Tente outro!"
            secure_client_socket.send(result.encode())
        return True

    def delete_all(self, msg, secure_client_socket, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")
        self.logger.info("Envia mensagem de confirmação para o cliente!")
        result_data = "'Tem certeza que deseja deletar todos os dados? (S/N)'"
        secure_client_socket.send(result_data.encode())

        confirm = secure_client_socket.recv(self.commands.SIZE.value).decode()
        
        if confirm == "s":
            self.data.delete_all()
            self.logger.info("Todos os dados foram deletados com sucesso!")
        
            result_data = "'Todos os dados foram deletados com sucesso!'"
            secure_client_socket.send(result_data.encode())
        else:
            self.logger.info("Operação cancelada pelo usuário!")
            result_data = "'Operação cancelada pelo usuário!'"
            secure_client_socket.send(result_data.encode())

        return True
    
    def delete_by_id(self, msg, secure_client_socket, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")
        self.logger.info("Enviando mensagem requisitando ao cliente o id do dado que deseja deletar!")

        result_data = "'Digite o id do dado que deseja deletar'"
        secure_client_socket.send(result_data.encode())

        data_id = secure_client_socket.recv(self.commands.SIZE.value).decode()
        self.logger.info(f"Recebendo do cliente o id: '{data_id}'")

        self.logger.info("Procurando elemento no banco de dados")
        result = self.data.get(int(data_id))

        if(result != None):
            self.logger.info("Enviando mensagem requisitando confirmação do usuário!")
            result = "1"
            secure_client_socket.send(result.encode())

            confirm = secure_client_socket.recv(self.commands.SIZE.value).decode()
            if confirm == "s":
                self.data.remove(int(data_id))
                self.logger.info("Dado deletado com sucesso!")

                result_data = "'Dado deletado com sucesso!'"
                secure_client_socket.send(result_data.encode())
            else:
                self.logger.info("Operação cancelada pelo usuário!")
                result_data = "'Operação cancelada pelo usuário!'"
                secure_client_socket.send(result_data.encode())
        else:
            self.logger.info("Usuario com id: '{data_id}' não encontrado!")
            result = "Usuário não encontrado! Tente outro!"
            secure_client_socket.send(result.encode())
        return True

    def finish(self, msg, address):
        self.logger.info(f"Mensagem recebida de {address} -> {msg}")
        self.logger.info("Finalizando comunicação com o cliente")
        return False