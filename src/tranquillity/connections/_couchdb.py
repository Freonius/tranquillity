'''
Module for CouchDb operations
'''
from typing import Callable, Set, Union
from couchdb import Server, Session, ServerError, Unauthorized, ResourceNotFound
from couchdb.client import Database
from .__interface import IConnection
from ..exceptions import ConnectionException


class CouchDb(IConnection):
    '''
    CouchDb connection.
    '''
    _client: Union[Server, None] = None
    _session: Session = Session()
    _token: Union[str, None] = None
    _db: Union[Database, None] = None

    def connect(self) -> None:
        _ks: Callable[[str], Set[str]] = lambda x: {
            x,
            f'couchdb.{x}',
            f'conns.couchdb.{x}'
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
        try:
            _url: str = f'{_protocol}://{_host}:{_port}'
            self._client = Server(url=_url, session=self._session,)
            self._log_debug(f'Connected to CouchDb {_url}')
            del _url
            if _username is not None and _password is not None:
                _token: Union[str, None] = self._client.login(
                    _username, _password,)
                if isinstance(_token, str):
                    self._token = _token
                else:
                    self._token = None
                del _token
        except ServerError:
            self._client = None
        except Unauthorized:
            self._client = None
        del _username, _password, _host, _port, _protocol
        if self._client is None:
            raise ConnectionException('Could not connect to CouchDB')
        _db_name: Union[str, None] = self._settings.lookup(_ks('db'))
        del _ks
        _db: Union[Database, None] = None
        try:
            if _db_name in self._client:
                _db = self._client[_db_name]
            else:
                _db = self._client.create(_db_name)
        except ResourceNotFound:
            _db = self._client.create(_db_name)
        self._db = _db

    def _is_connected(self) -> bool:
        # pylint: disable=broad-except
        if self._client is None:
            return False
        if self._token is None:
            try:
                return bool(self._client)
            except Exception:
                return False
        return bool(self._client.verify_token(self._token))
        # pylint: enable=broad-except

    def close(self) -> None:
        if self._token is not None and self._client is not None:
            self._client.logout(self._token)
        self._db = None
        self._token = None
        self._client = None
