'''
Module for Elasticsearch operations
'''
from typing import Union, Tuple, Iterator, Type
from elasticsearch.client import Elasticsearch as ES
from ..exceptions import ConnectionException
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
        if id is not None:
            id
        self.client.search(index=t.get_table(), body={})
        raise NotImplementedError

    def insert(self, obj: T) -> Tuple[Union[T, None], IdType, bool]:
        return super().insert(obj)

    def update(self, obj: T, /, id: IdType = None, where: WhereType = None) -> Tuple[Union[T, None], bool]:
        return super().update(obj, id, where)

    def delete(self, obj: T) -> bool:
        pass

    def delete_where(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> int:
        return super().delete_where(t, id, where)
