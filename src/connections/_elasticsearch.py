'''
Module for Elasticsearch operations
'''
from typing import Dict, Union, Tuple, Iterator, Type, Any
from elasticsearch.client import Elasticsearch as ES
from json import loads
from ..exceptions import ConnectionException
from ..query._where import _wc2es, _id2wc
from .__interface import IConnection
from .__alias import T, IdType, WhereType


class Elasticsearch(IConnection):
    '''
    Elasticsearch connection.
    '''
    _client: Union[ES, None] = None

    def connect(self) -> None:
        _host: Union[str, None] = self._settings.get('conn.elasticsearch.host')
        if _host is None:
            raise ConnectionException('host is not defined')
        _port: Union[int, None]
        if (_port := self._settings.get_int('conn.elasticsearch.port', 9200)) is None:
            _port = 9200
        _protocol: Union[str, None] = None
        try:
            _protocol = self._settings.get(
                'conn.elasticsearch.protocol', 'http')
        except KeyError:
            pass
        if _protocol is None:
            _protocol = 'http'
        _username: Union[str, None] = None
        _password: Union[str, None] = None
        try:
            _username = self._settings.get('conn.elasticsearch.user')
            _password = self._settings.get('conn.elasticsearch.password')
        except KeyError:
            pass
        _url: str = f'{_protocol}://'
        del _protocol
        if _username is not None and _password is not None:
            _url += f'{_username}:{_password}@'
        del _username, _password
        _url += f'{_host}:{_port}'
        _client: ES = ES(_url)
        self._client = _client

    def _is_connected(self) -> bool:
        if self._client is None:
            return False
        return self._client.ping()

    def close(self) -> None:
        if self._client is None:
            return
        self._client.close()
        self._client = None

    @property
    def client(self) -> ES:
        if self._client is None:
            raise ConnectionException('Client is None')
        return self._client

    def select(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> Iterator[T]:
        if where is None:
            where = []
        if id is not None and (_field_id := t.get_id_field()) is not None:
            where.append(_id2wc(_field_id, id))
            del _field_id
        res = self.client.search(
            index=t.get_table(), body={'query': loads(_wc2es(where)[0])})
        if 'hits' in res.keys():
            if len(res['hits']):
                if 'hits' in res['hits'].keys():
                    for r in [t(**x['_source'], **{str(t.get_id_field()): x['_id']}) for x in res['hits']['hits']]:
                        yield r

    def insert(self, obj: T) -> Tuple[Union[T, None], IdType, bool]:
        if obj.get_id_field() is None:
            raise ValueError('Object must have an id field')
        _body: Dict[str, Any] = obj.serialize()
        if '_id' in _body.keys():
            _body.pop('_id')
        if not isinstance((_res := self.client.index(obj.get_table(), body=_body)), dict):
            return None, None, False
        del _body
        if 'result' not in _res.keys() or _res['result'] != 'created':
            return None, None, False
        if '_id' not in _res.keys() or not isinstance(_res['_id'], str):
            return None, None, False
        obj.set_id(_res['_id'])
        return obj, _res['_id'], True

    def update(self, obj: T, /, id: IdType = None, where: WhereType = None) -> Tuple[Union[T, None], bool]:
        if where is None:
            where = []
        if id is None:
            id = obj.get_id()
        if id is not None and (_field_id := obj.get_id_field()) is not None:
            where.append(_id2wc(_field_id, id))
            del _field_id
        # _q = loads(_wc2es(where)[0])
        _body: Dict[str, Any] = obj.serialize()
        if '_id' in _body.keys():
            _body.pop('_id')
        _res = self.client.update(
            obj.get_table(), body={'doc': _body}, id=obj.get_id())
        if not isinstance(_res, dict):
            return obj, False
        del _body
        if 'result' not in _res.keys() or _res['result'] != 'updated':
            return obj, False
        if '_id' not in _res.keys() or not isinstance(_res['_id'], str):
            return obj, False
        return obj, True

    def delete_where(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> int:
        if where is None:
            where = []
        if id is not None and (_field_id := t.get_id_field()) is not None:
            where.append(_id2wc(_field_id, id))
            del _field_id
        _q = loads(_wc2es(where)[0])
        _res = self.client.delete_by_query(t.get_table(), body={'query': _q})
        if not isinstance(_res, dict):
            return 0
        _out = 0
        if 'deleted' not in _res.keys():
            return 0
        if not isinstance((_out := _res['deleted']), int):
            return 0
        return _out

    def add_mapping(self, index: str, mapping: Dict[str, Dict[str, Dict[str, Dict[str, Union[str, bool]]]]]) -> bool:
        _res = self.client.indices.create(
            index=index,
            body=mapping,
            ignore=400
        )
        if isinstance(_res, dict) and 'acknowledged' in _res.keys() and isinstance(_res['acknowledged'], bool):
            return _res['acknowledged']
        return False

    def create_table(self, t: Type[T]) -> bool:
        return self.add_mapping(t.get_table(), t.to_es_mapping())

    def drop_table(self, t: Type[T]) -> bool:
        _res = self.client.indices.delete(t.get_table(), ignore=404)
        if isinstance(_res, dict) and 'acknowledged' in _res.keys() and isinstance(_res['acknowledged'], bool):
            return _res['acknowledged']
        return False
