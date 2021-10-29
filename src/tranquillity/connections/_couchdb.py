from typing import Union
from couchdb import Server, Session, ServerError
from couchdb.client import Database
from ..interfaces import IConnection

class CouchDb(IConnection):
    _client: Union[Server, None] = None
    _session: Session = Session()

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
            if _username is not None and _password is not None:
                self._client = Server(
                    url=f'{_protocol}://{_username}:{_password}@{_host}:{_port}',
                    session=self._session,)
            else:
                self._client = Server(url=f'{_protocol}://{_host}:{_port}', session=self._session,)
        except ServerError:
            self._client = None
        del _username, _password, _host, _port, _protocol
        _db_name: str = self._settings['couchdb.db']
        _db: Database
        try:
            _db = self._client[_db_name]
        except Exception:
            _db = self._client.create(_db_name)
        