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