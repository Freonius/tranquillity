'''
Module for Elasticsearch operations
'''
from typing import Union
from elasticsearch.client import Elasticsearch as ES
from .__interface import IConnection
from tranquillity.exceptions import ConnectionException


class Elasticsearch(IConnection):
    '''
    Elasticsearch connection.
    '''
    _client: Union[ES, None] = None

    def connect(self) -> None:
        _host: Union[str, None] = self._settings.get('conn.elasticsearch.host')
        if _host is None:
            raise ConnectionException('host is not defined')
        _port: int = self._settings.get_int('conn.elasticsearch.port', 9200)
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