# Trabalho para a disciplina Tópicos em Redes 
# Sistema cliente/servidor com comunicação segura
# Autores: Gustavo Valente Nunes | GRR: 20182557 
#          Henrique Prokopenko | GRR20186712
# Data: 31/05/2023

class HashTable:

    def __init__(self):
        self.table = {}
        self.id = 0

    def insert(self, value):
        if value not in self.table.values():
            self.id += 1
            self.table[self.id] = value
            return True

        return False

    def get(self, key):
        return self.table.get(key)

    def remove(self, key):
        if key in self.table:
            del self.table[key]

    def delete_all(self):
        self.table.clear()

    def update(self, key, new_value):
        self.table[key] = new_value


    def __str__(self):
        return str(self.table)