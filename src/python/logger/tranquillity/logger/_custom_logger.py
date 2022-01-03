from sys import stdout
from logging import DEBUG, INFO, ERROR, WARNING, Logger, StreamHandler, Formatter, FileHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
# pylint: disable=redefined-builtin
from re import compile, Pattern, Match, finditer, match
# pylint: enable=redefined-builtin
from datetime import datetime, date, time
from typing import List, Union, Callable, Set, Tuple, Dict, Any
import asyncio
from pickle import dumps
from json import dumps as jdumps
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from elasticsearch import AsyncElasticsearch, Elasticsearch
from tranquillity.shell import Shell
from tranquillity.settings import ISettings, Yaml
from tranquillity.exceptions import ConnectionException
from ._enum import LogType
from .__interfaces import ILogHandler
from .__custom_log_record import CustomLogRecord, _lr2d, _d2lr

# filterwarnings('ignore')


class CustomLogger(Logger):
    _settings: ISettings

    def _calc_level(self, _log_name: str) -> int:
        level: int = DEBUG
        try:
            _val: str = self._settings.get_ns(
                f'log.loggers.{_log_name}.level').upper().strip()
            if _val == 'DEBUG':
                level = DEBUG
            if _val == 'INFO':
                level = INFO
            if _val == 'WARNING':
                level = WARNING
            if _val == 'ERROR':
                level = ERROR
            del _val
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
        except KeyError:
            pass

        if frmt is None:
            self.frmt = f'[{module_name}@{Shell.get_docker_id()}' + \
                ':%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s'
        else:
            self.frmt = frmt
        self.level = level
        self.name_log_file = name_log_file
        self.module_name = module_name
        self.output = {DEBUG: '', INFO: '', ERROR: '', WARNING: ''}
        self.formatter = Formatter(self.frmt)
        super().__init__(name=name_log_file, level=level)
        self._add_custom_handlers(settings)
        self._add_rotation_handler(settings)

    def _add_custom_handlers(self, settings: ISettings) -> None:
        try:
            if settings.get_bool('log.loggers.file.enabled'):
                self.add_custom_handler(LogType.FILE, self._calc_level('file'))
        except KeyError:
            pass
        try:
            if settings.get_bool('log.loggers.stream.enabled'):
                self.add_custom_handler(
                    LogType.STREAM, self._calc_level('stream'))
        except KeyError:
            pass
        try:
            if settings.get_bool('log.loggers.sql.enabled'):
                self.add_custom_handler(LogType.SQL, self._calc_level('sql'))
        except KeyError:
            pass
        try:
            if settings.get_bool('log.loggers.rabbitmq.enabled'):
                self.add_custom_handler(
                    LogType.RABBITMQ, self._calc_level('rabbitmq'))
        except KeyError:
            pass
        try:
            if settings.get_bool('log.loggers.elasticsearch.enabled'):
                self.add_custom_handler(
                    LogType.ELASTIC, self._calc_level('elasticsearch'))
        except KeyError:
            pass

    def _add_rotation_handler(self, settings: ISettings) -> None:
        _rotation_enabled: bool = False
        try:
            if settings.get_bool('log.rotation.enabled'):
                _rotation_enabled = True
        except KeyError:
            _rotation_enabled = False
        _daily: bool = False
        try:
            _daily = settings.get_bool('log.rotation.daily')
        except KeyError:
            _daily = False
        _keep: int = 10
        try:
            _keep = settings.get_int('log.rotation.keep')
        except KeyError:
            _keep = 10
        try:
            _size: Union[str, None] = settings.get('log.rotation.size')
            _bytes: int = 0
            if _size is not None:
                _size = _size.strip().upper()
                _m_size: Union[Match, None] = match(
                    r'^(\d+)(KB?|MB?)?$', _size)
                if _m_size is not None:
                    _digits: int = int(_m_size.group(1))
                    _size_part: str = _m_size.group(2)
                    if _size_part in {'K', 'KB'}:
                        _digits *= 1024
                    elif _size_part in {'M', 'MB'}:
                        _digits *= 1024
                        _digits *= 1024
                    _bytes = _digits
            if _rotation_enabled and _bytes > 0:
                self.addHandler(
                    RotatingFileHandler(self.name_log_file, backupCount=_keep))
        except KeyError:
            pass
        if _rotation_enabled and _daily:
            self.addHandler(TimedRotatingFileHandler(
                self.name_log_file, when='d'))

    def add_custom_handler(self,
                           logtype: LogType,
                           level: Union[int, None] = None,
                           override_name: Union[str, None] = None):
        console_logger: Union[StreamHandler, ElasticLogHandler,
                              SqlLogHandler, FileHandler, RabbitLogHandler]
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
    _client: AsyncElasticsearch

    def __init__(self, settings: ISettings):
        super().__init__(settings)
        self._client = AsyncElasticsearch(
            self._settings.get('conn.elasticsearch.host', 'es') +
            ':' + str(self._settings.get('conn.elasticsearch.port', '9200')))

    def _custom_emit(self, record: CustomLogRecord) -> None:
        async def _asemit(record: CustomLogRecord, index: str, client: AsyncElasticsearch):
            await client.index(index, body=jdumps(_lr2d(record)))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(_asemit(record,
                                        self._settings.get(
                                            'log.loggers.elasticsearch.index', 'logs'),
                                        self._client))

    @staticmethod
    def get_log_record(
        settings: Union[ISettings, None] = None,
        term: Union[str, None] = None,
        filename: Union[str, None] = None,
        date_filter: Union[datetime,
                           Tuple[datetime, datetime], date, None] = None,
        module: Union[str, None] = None,
        level: Union[str, int, None] = None,
    ) -> List[CustomLogRecord]:
        if settings is None:
            settings = Yaml()
        _index: str = settings.get(
            'log.loggers.elasticsearch.index', 'logs')
        _client: Elasticsearch = Elasticsearch(settings.get('conn.elasticsearch.host', 'es') +
                                               ':' + str(settings.get('conn.elasticsearch.port', '9200')))
        query: Dict[str, Dict[str, Any]] = {}
        if isinstance(date_filter, date):
            date_filter = (datetime.combine(date_filter, time(
                0, 0, 0)), datetime.combine(date_filter, time(23, 59, 59)))
        if isinstance(date_filter, tuple):
            query['range'] = {}
            query['range']['time'] = {
                'gte': date_filter[0],
                'lte': date_filter[1]
            }
        elif isinstance(date_filter, datetime):
            query['match'] = {'time': date_filter}
        if term is not None:
            if 'match' not in query.keys():
                query['match'] = {}
            query['match']['message'] = term
        if level is not None:
            if isinstance(level, int):
                if level is DEBUG:
                    level = 'DEBUG'
                elif level is INFO:
                    level = 'INFO'
                elif level is WARNING:
                    level = 'WARNING'
                elif level is ERROR:
                    level = 'ERROR'
                else:
                    level = 'UNKNOWN'
            level = level.upper().strip()
            if 'match' not in query.keys():
                query['match'] = {}
            query['match']['level'] = level
        if filename is not None:
            if 'match' not in query.keys():
                query['match'] = {}
            query['match']['filename'] = filename
        if module is not None:
            if 'match' not in query.keys():
                query['match'] = {}
            query['match']['module'] = module
        if 'match' in query.keys() and len(query['match']) > 1 and len(query.keys()) == 1:
            query = {'bool': {
                'must': [{'match': {k: query['match'][k]}} for k in query['match'].keys()]}}
        elif len(query.keys()) > 1:
            if 'match' in query.keys() and len(query['match']) > 1:
                temp_query = {'bool': {
                    'must': [{'match': {k: query['match'][k]}} for k in query['match'].keys()]}}
                temp_query['bool']['must'].extend(
                    [{k: query[k]} for k in query.keys() if k != 'match'])
                query = temp_query
            else:
                query = {'bool': {'must': [{k: query[k]}
                                           for k in query.keys()]}}
        elif len(query.keys()) == 0:
            query['match_all'] = {}
        res = _client.search(index=_index, body={'query': query})
        if 'hits' in res.keys():
            if len(res['hits']):
                if 'hits' in res['hits'].keys():
                    return [_d2lr(x['_source']) for x in res['hits']['hits']]
        return []


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
        # _protocol: Union[str, None] = None
        # try:
        #     _protocol = self._settings.lookup(_ks('protocol'), 'http')
        # except KeyError:
        #     pass
        # if _protocol is None:
        #     _protocol = 'http'
        _username: Union[str, None] = None
        _password: Union[str, None] = None
        try:
            _username = self._settings.lookup(_ks('user'))
            _password = self._settings.lookup(_ks('password'))
        except KeyError:
            pass
        _credentials: PlainCredentials
        if _username is None or \
            _username.strip() == '' or \
            _password is None or \
                _password.strip() == '':
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
            exchange='', routing_key=self._queue, body=dumps(_lr2d(record)))

    @staticmethod
    def rabbit_log_listener():
        pass


class SqlLogHandler(ILogHandler):

    def _custom_emit(self, record: CustomLogRecord) -> None:
        pass
