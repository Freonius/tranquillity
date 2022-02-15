from datetime import datetime, date, time
from typing import List, Union, Tuple, Dict, Any, Awaitable, TypeVar
from logging import INFO, DEBUG, WARNING, ERROR
from json import dumps as jdumps
import asyncio
import nest_asyncio
from threading import Thread
from elasticsearch import AsyncElasticsearch, Elasticsearch
from ..settings import ISettings, Yaml
from ..exceptions import ConnectionException
from .__custom_log_record import CustomLogRecord, _d2lr, _lr2d
from .__interfaces import ILogHandler

T = TypeVar('T')


def _start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


_LOOP = asyncio.new_event_loop()
_LOOP_THREAD = Thread(
    target=_start_background_loop, args=(_LOOP,), daemon=True
)
_LOOP_THREAD.start()


def asyncio_run(coro: Awaitable[T], timeout=30) -> T:
    return asyncio.run_coroutine_threadsafe(coro, _LOOP).result(timeout=timeout)


def _convert_int2level(level: int) -> str:
    if level is DEBUG:
        return 'DEBUG'  # pragma: no cover
    if level is INFO:
        return 'INFO'
    if level is WARNING:
        return 'WARNING'  # pragma: no cover
    if level is ERROR:
        return 'ERROR'
    return 'UNKNOWN'


class ElasticLogHandler(ILogHandler):
    _client: AsyncElasticsearch

    @staticmethod
    def _get_url(settings: ISettings) -> str:
        _host: Union[str, None] = settings.get('conn.elasticsearch.host')
        if _host is None:
            raise ConnectionException('host is not defined')
        _port: Union[int, None]
        if (_port := settings.get_int('conn.elasticsearch.port', 9200)) is None:
            _port = 9200
        _protocol: Union[str, None] = None
        try:
            _protocol = settings.get(
                'conn.elasticsearch.protocol', 'http')
        except KeyError:
            pass
        if _protocol is None:
            _protocol = 'http'
        _username: Union[str, None] = None
        _password: Union[str, None] = None
        try:
            _username = settings.get('conn.elasticsearch.user')
            _password = settings.get('conn.elasticsearch.password')
        except KeyError:
            pass
        _url: str = f'{_protocol}://'
        del _protocol
        if _username is not None and _password is not None:
            _url += f'{_username}:{_password}@'
        del _username, _password
        _url += f'{_host}:{_port}'
        return _url

    def __init__(self, settings: ISettings):
        nest_asyncio.apply()
        super().__init__(settings)

        self._client = AsyncElasticsearch(self._get_url(self._settings))

    def _custom_emit(self, record: CustomLogRecord) -> None:
        async def _asemit(record: CustomLogRecord, index: str, client: AsyncElasticsearch):
            await client.index(index, body=jdumps(_lr2d(record)))

        asyncio_run(_asemit(record,
                            self._settings.get_ns(
                                'log.loggers.elasticsearch.index'),
                            self._client))

    # pylint: disable=too-many-arguments,too-many-branches
    @classmethod
    def get_log_record(cls,
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
        _index: str = str(settings.get(
            'log.loggers.elasticsearch.index', 'logs'))
        _client: Elasticsearch = Elasticsearch(cls._get_url(settings))
        query: Dict[str, Dict[str, Any]] = {}
        if isinstance(date_filter, date):
            date_filter = (datetime.combine(date_filter, time(
                0, 0, 0)), datetime.combine(date_filter, time(23, 59, 59)))
        if isinstance(date_filter, tuple):
            query['range'] = {}
            query['range']['time'] = {
                'gte': date_filter[0].isoformat(),
                'lte': date_filter[1].isoformat(),
            }
        if isinstance(date_filter, datetime):
            query['match'] = {
                'time': date_filter.isoformat()}
        if term is not None:
            if 'match' not in query.keys():
                query['match'] = {}
            query['match']['message'] = term
        if level is not None:
            if isinstance(level, int):
                level = _convert_int2level(level)
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
                    [{k: i} for k, i in query.items() if k != 'match'])
                query = temp_query
            else:
                query = {'bool': {'must': [{k: i}
                                           for k, i in query.items()]}}
        elif len(query.keys()) == 0:
            query['match_all'] = {}
        res = _client.search(index=_index, body={'query': query})
        if 'hits' in res.keys():
            if len(res['hits']):
                if 'hits' in res['hits'].keys():
                    return [_d2lr(x['_source']) for x in res['hits']['hits']]
        return []
    # pylint: enable=too-many-arguments,too-many-branches
