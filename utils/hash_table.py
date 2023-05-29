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

    def __str__(self):
        return str(self.table)