from typing import Union
from couchdb import Server, Session, ServerError, Unauthorized, ResourceNotFound
from couchdb.client import Database
from ..interfaces import IConnection
from ..exceptions import ConnectionException

class CouchDb(IConnection):
    _client: Union[Server, None] = None
    _session: Session = Session()
    _token: Union[str, None] = None
    _db: Union[Database, None] = None

    def connect(self) -> None:
        _host: str = self._settings['couchdb.host']
        _port: int = int(self._settings['couchdb.port'])
        _protocol: Union[str, None] = None
        try:
            _protocol = self._settings['couchdb.protocol']
        except KeyError:
            pass
        if _protocol is None:
            _protocol = 'http'
        # TODO: Check whether there are session params
        _username: Union[str, None] = None
        _password: Union[str, None] = None
        try:
            _username = self._settings['couchdb.user']
            _password = self._settings['couchdb.password']
        except KeyError:
            pass
        try:
            _url: str = f'{_protocol}://{_host}:{_port}'
            self._client = Server(url=_url, session=self._session,)
            self._log_debug(f'Connected to CouchDb {_url}')
            del _url
            if _username is not None and _password is not None:
                _token: Union[str, None] = self._client.login(_username, _password,)
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
        _db_name: str = self._settings['couchdb.db']
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
        if self._client is None:
            return False
        if self._token is None:
            try:
                return bool(self._client)
            except Exception:
                return False
        return bool(self._client.verify_token(self._token))

    def close(self) -> None:
        if self._token is not None and self._client is not None:
            self._client.logout(self._token)
        self._db = None
        self._token = None
        self._client = None
        