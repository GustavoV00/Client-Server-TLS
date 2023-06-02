# Trabalho para a disciplina Tópicos em Redes 
# Sistema cliente/servidor com comunicação segura
# Autores: Gustavo Valente Nunes | GRR: 20182557 
#          Henrique Prokopenko | GRR20186712
# Data: 31/05/2023

from utils import utils


class ClientService(object):
    def __init__(self, logger, connection, size) -> None:
        self.logger = logger
        self.connection = connection
        self.size = size

    def get_all(self, option):
        self.logger.info("Enviando mensagem para 'Consultar todos os dados'!")
        utils.send_message(option, self.logger, self.connection)
        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

    def get_by_id(self, option):
        self.logger.info("Enviando mensagem para 'Consultar dado por id'!")
        utils.send_message(option, self.logger, self.connection)

        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

        data_id = input("Digite o id: ")
        
        # Testa o input até receber um id que seja um número válido.
        while data_id.isdigit() == False:
            print("Apenas números são permitidos!")
            data_id = input("Digite o id: ")

        utils.send_message(data_id, self.logger, self.connection)

        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: '{resposta}'")

    def create(self, option):
        self.logger.info("Enviando mensagem para 'Criar um novo dado'!")
        utils.send_message(option, self.logger, self.connection)

        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

        user = input("Digite o novo usuario: ")
        utils.send_message(user, self.logger, self.connection)

        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

    def update_by_id(self, option):
        self.logger.info("Enviando mensagem para 'Atualizar um dado'!")
        utils.send_message(option, self.logger, self.connection)

        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

        user = input("Digite o id: ")

        # Testa o input até receber um id de usuário que seja um número válido.
        while user.isdigit() == False:
            print("Apenas números são permitidos!")
            user = input("Digite o id: ")

        utils.send_message(user, self.logger, self.connection)

        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

        user = input("Digite o nome do usuario para atualizar: ")
        utils.send_message(user, self.logger, self.connection)

        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

    def delete_all(self, option):
        self.logger.info("Enviando mensagem para 'Deletar todos os dados'!")
        utils.send_message(option, self.logger, self.connection)
        resposta = utils.recv_message(self.logger, self.connection, self.size)

        self.logger.info(f"Resposta recebida do servidor: {resposta}")
        confirm = input("Deseja realmente deletar todos os dados? (s/n): ")
        
        # Confirmação para excluir todos os dados
        while confirm != "s" and confirm != "n":
            print("Opção inválida!")
            confirm = input("Deseja realmente deletar todos os dados? (s/n): ")

        utils.send_message(confirm, self.logger, self.connection)
        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

    def delete_by_id(self, option):
        self.logger.info("Enviando mensagem para 'Deletar dado por id'!")
        utils.send_message(option, self.logger, self.connection)

        resposta = utils.recv_message(self.logger, self.connection, self.size)
        self.logger.info(f"Resposta recebida do servidor: {resposta}")

        user = input("Digite o id: ")

        # Verifica se um id válido
        while user.isdigit() == False:
            print("Apenas números são permitidos!")
            user = input("Digite o id: ")

        utils.send_message(user, self.logger, self.connection)

        resposta = utils.recv_message(self.logger, self.connection, self.size)

        if resposta == "1":
            self.logger.info(f"Resposta recebida do servidor: {resposta}")
            confirm = input("Deseja realmente deletar o dado? (s/n): ")

            while confirm != "s" and confirm != "n":
                print("Opção inválida!")
                confirm = input("Deseja realmente deletar o dado? (s/n): ")

            utils.send_message(confirm, self.logger, self.connection)

            resposta = utils.recv_message(self.logger, self.connection, self.size)

        self.logger.info(f"Resposta recebida do servidor: {resposta}")

    def finish(self, option):
        self.logger.info("Finalizando a comunicação com o servidor!")
        utils.send_message(option, self.logger, self.connection)