# Trabalho para a disciplina Tópicos em Redes 
# Sistema cliente/servidor com comunicação segura
# Autores: Gustavo Valente Nunes | GRR: 20182557 
#          Henrique Prokopenko | GRR20186712
# Data: 31/05/2023

from enum import Enum


class Commands(Enum):
    FINISH=0
    GET_ALL=1
    GET_BY_ID=2
    CREATE=3
    UPDATE_BY_ID=4
    DELETE_ALL=5
    DELETE_BY_ID=6
    SIZE=8192
