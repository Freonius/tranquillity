from enum import Enum, IntFlag, auto


class ConnType(Enum):
    COUCHDB = auto()
    ELASTICSEARCH = auto()
    MONGO = auto()
    SQLITE = auto()
    MYSQL = auto()
    PGSQL = auto()
    DB2 = auto()
    MSSQL = auto()
    HAZELCAST = auto()
    SPRING_CONFIG = auto()
    KAFKA = auto()
    MQQT = auto()
    RABBIT = auto()
    REDIS = auto()
    EUREKA = auto()
    ORACLE = auto()


class HttpVerb(Enum):
    HEAD = 'HEAD'
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


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
