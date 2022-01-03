from datetime import datetime, date, time
from typing import List, Union, Tuple, Dict, Any
from logging import INFO, DEBUG, WARNING, ERROR
from json import dumps as jdumps
import asyncio
from elasticsearch import AsyncElasticsearch, Elasticsearch
from tranquillity.settings import ISettings, Yaml
from .__custom_log_record import CustomLogRecord, _d2lr, _lr2d
from .__interfaces import ILogHandler


def _convert_int2level(level: int) -> str:
    if level is DEBUG:
        return 'DEBUG'  # pragma: no cover
    if level is INFO:
        return 'INFO'
    if level is WARNING:
        return 'WARNING' # pragma: no cover
    if level is ERROR:
        return 'ERROR'
    return 'UNKNOWN'


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

    # pylint: disable=too-many-arguments,too-many-branches
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
        _client: Elasticsearch = Elasticsearch(
            settings.get('conn.elasticsearch.host', 'es') +
            ':' + str(settings.get('conn.elasticsearch.port', '9200')))
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
