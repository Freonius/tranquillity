from enum import Enum, IntFlag, auto

class SettingsType(Enum):
    ENV = auto()
    SQLITE = auto()
    API = auto()
    YAML = auto()
    INI = auto()
    PROPERTIES = auto()
    DICT = auto()
    CSV = auto()
    JSON = auto()
    BSON = auto()
    PICKLE = auto()
    SPRING = auto()

class LogType(Enum):
    FILE = auto()
    STREAM = auto()
    SQL = auto()
    ELASTIC = auto()
    RABBITMQ = auto()

class Allowance(IntFlag):
    NONE = 0
    READ = 1
    WRITE = 2
    ADD = 4
    DELETE = 8

class Role(Enum):
    ADMIN = Allowance.ADD + Allowance.DELETE + Allowance.READ + Allowance.WRITE
    READ_ONLY = Allowance.READ
    READ_WRITE = Allowance.ADD + Allowance.READ + Allowance.WRITE
    UNAUTHORIZED = Allowance.NONE
