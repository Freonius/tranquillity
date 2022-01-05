'''
Module for Mongo operations
'''
from typing import Callable, Set, Union
from urllib.parse import quote_plus
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.database import Database
from tranquillity.exceptions import ConnectionException
from .__interface import IConnection


class Mongo(IConnection):
    '''
    Mongo connection.
    '''
    _client: Union[MongoClient, None] = None
    _db: Union[Database, None] = None

    def connect(self) -> None:
        _ks: Callable[[str], Set[str]] = lambda x: {
            x,
            f'mongo.{x}',
            f'conn.mongo.{x}'
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
        _url: str = 'mongodb://'
        if not (_username is None or _username.strip() == '' or _password is None or _password.strip() == ''):
            _url += f'{quote_plus(_username)}:{quote_plus(_password)}@'
        _url += _host
        try:

            self._client = MongoClient(host=_url, port=_port,)
            self._log_debug(f'Connected to MongoDb {_host}:{_port}')
        except ConnectionFailure:
            self._client = None
        del _username, _password, _host, _port, _protocol, _url
        if self._client is None:
            raise ConnectionException('Could not connect to MongoDB')
        _db_name: str = self._settings.lookup_ns(_ks('db'))
        del _ks
        _db: Union[Database, None] = None
        try:
            _db = self._client.get_database(_db_name)
        except Exception:
            _db = None
        self._db = _db

    def close(self) -> None:
        if self._client is None:
            return
        if self._is_connected() is False:
            self._client = None
            return
        self._client.close()

    def _is_connected(self) -> bool:
        if self._client is None:
            return False
        try:
            self._client.admin.command('ismaster')
            return True
        except ConnectionFailure:
            return False

    @property
    def client(self) -> MongoClient:
        if self._client is None:
            raise ConnectionError
        return self._client


if __name__ == '__main__':
    m = Mongo()
    with m:
        print(m.is_connected)
        m.client
