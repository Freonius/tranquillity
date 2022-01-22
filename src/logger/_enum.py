from enum import Enum, auto


class LogType(Enum):
    FILE = auto()
    STREAM = auto()
    SQL = auto()
    ELASTIC = auto()
    RABBITMQ = auto()
