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
