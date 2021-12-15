from os import sep
from sys import stdout
from logging import DEBUG, INFO, ERROR, WARNING, LogRecord, Logger, StreamHandler, getLoggerClass, Formatter, FileHandler
from typing import Union
from re import compile, Pattern, Match, finditer
from typing import Union, Callable, Set
from pickle import dumps, loads
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from .__interfaces import ILogHandler
from tranquillity.shell import Shell
from tranquillity.settings import ISettings, Yaml
from tranquillity.enums import LogType
from .__custom_log_record import CustomLogRecordException, CustomLogRecord

# filterwarnings('ignore')


class CustomLogger(Logger):
    _settings: ISettings

    def _calc_level(self, _log_name: str) -> int:
        level: int = DEBUG
        try:
            match self._settings.get_ns(f'log.loggers.{_log_name}.level').upper().strip():
                case 'DEBUG':
                    level = DEBUG
                case 'INFO':
                    level = INFO
                case 'WARNING':
                    level = WARNING
                case 'ERROR':
                    level = ERROR
        except KeyError:
            pass
        if level is DEBUG and not __debug__:
            level = INFO
        return level

    def __init__(self, settings: Union[ISettings, None] = None):

        if settings is None:
            settings = Yaml()
        self._settings = settings
        level: int = self._calc_level('file')
        _ptrn: Pattern = compile(r'\{\{\s*([a-z\.]+)\s*\}\}')
        _m: Match
        name_log_file: str = settings.get_ns('log.loggers.file.file')

        for _m in finditer(_ptrn, name_log_file):
            name_log_file = name_log_file.replace(
                _m.group(0), settings.get_ns(_m.group(1)), 1)
            del _m

        del _ptrn

        module_name: str = settings.get_ns('app.name')
        frmt: Union[str, None] = None

        try:
            frmt = settings.get('log.format')
        except Exception:
            pass

        if frmt is None:
            self.frmt = '[{}@{}'.format(
                module_name, Shell.get_docker_id()) + ':%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s'
        else:
            self.frmt = frmt

        self.level = level
        self.name_log_file = name_log_file
        self.module_name = module_name
        self.output = {DEBUG: '', INFO: '', ERROR: '', WARNING: ''}
        self.formatter = Formatter(self.frmt)
        super().__init__(name=name_log_file, level=level)
        if settings.get_bool('log.loggers.file.enabled'):
            self.add_custom_handler(LogType.FILE, self._calc_level('file'))
        if settings.get_bool('log.loggers.stream.enabled'):
            self.add_custom_handler(LogType.STREAM, self._calc_level('stream'))
        if settings.get_bool('log.loggers.sql.enabled'):
            self.add_custom_handler(LogType.SQL, self._calc_level('sql'))
        if settings.get_bool('log.loggers.rabbitmq.enabled'):
            self.add_custom_handler(
                LogType.RABBITMQ, self._calc_level('rabbitmq'))
        if settings.get_bool('log.loggers.elasticsearch.enabled'):
            self.add_custom_handler(
                LogType.ELASTIC, self._calc_level('elasticsearch'))

    def add_custom_handler(self, logtype: LogType, level: Union[int, None] = None, override_name: Union[str, None] = None):
        if logtype is LogType.STREAM:
            console_logger = StreamHandler(stdout)
        elif logtype is LogType.ELASTIC:
            console_logger = ElasticLogHandler(self._settings)
        # elif logtype is LogType.MONGO:
        #     console_logger = mongo_log_handler(
        #         self.module_name, self._settings)
        elif logtype is LogType.SQL:
            console_logger = SqlLogHandler(self._settings)
        elif logtype is LogType.FILE:
            if override_name is None:
                console_logger = FileHandler(self.name_log_file)
            else:
                console_logger = FileHandler(override_name)
        elif logtype is LogType.RABBITMQ:
            console_logger = RabbitLogHandler(self._settings)
        else:
            return
        if level is None:
            console_logger.setLevel(self.level)
        else:
            console_logger.setLevel(level)
        console_logger.setFormatter(self.formatter)
        self.addHandler(console_logger)


class ElasticLogHandler(ILogHandler):
    _client = ''

    def __init__(self, settings: ISettings):
        super().__init__(settings)

    def _custom_emit(self, record: CustomLogRecord) -> None:
        pass


# class mongo_log_handler(ILogHandler):
#     def _custom_emit(self, record: CustomLogRecord) -> None:
#         m = Mongo(self._settings)
#         m.add(record)
#         m.close()


class RabbitLogHandler(ILogHandler):
    _queue: str
    _client: BlockingConnection
    _channel: BlockingChannel

    def __init__(self, settings: ISettings):
        super().__init__(settings)
        self.initialize_client()

    # @staticmethod
    def initialize_client(self) -> None:
        _ks: Callable[[str], Set[str]] = lambda x: {
            x,
            f'rabbitmq.{x}',
            f'conns.rabbitmq.{x}',
            f'rabbit.{x}',
            f'conn.rabbit.{x}',
        }
        _host: Union[str, None] = self._settings.lookup(_ks('host'))
        if _host is None:
            raise ConnectionException('host is not defined')
        _port: int = int(str(self._settings.lookup(_ks('port'), '5984')))
        _protocol: Union[str, None] = None
        try:
            _protocol = self._settings.lookup(_ks('protocol'), 'http')
        except KeyError:
            pass
        if _protocol is None:
            _protocol = 'http'
        _username: Union[str, None] = None
        _password: Union[str, None] = None
        try:
            _username = self._settings.lookup(_ks('user'))
            _password = self._settings.lookup(_ks('password'))
        except KeyError:
            pass
        _credentials: PlainCredentials
        if _username is None or _username.strip() == '' or _password is None or _password.strip() == '':
            _credentials = ConnectionParameters.DEFAULT_CREDENTIALS
        else:
            _credentials = PlainCredentials(_username, _password)
        self._client = BlockingConnection(ConnectionParameters(
            host=_host, port=_port, credentials=_credentials))
        self._queue = self._settings.lookup_ns(_ks('queue'))
        self._channel = self._client.channel()

    def _custom_emit(self, record: CustomLogRecord) -> None:
        self._channel.queue_declare(queue=self._queue)
        self._channel.basic_publish(
            exchange='', routing_key=self._queue, body=dumps(dict(record)))

    @staticmethod
    def rabbit_log_listener():
        pass


class SqlLogHandler(ILogHandler):

    def _custom_emit(self, record: CustomLogRecord) -> None:
        pass
