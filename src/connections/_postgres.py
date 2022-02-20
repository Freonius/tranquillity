
from typing import List, Union, Dict, Tuple, Iterator, Type
from psycopg2 import connect
from psycopg2._psycopg import connection
from psycopg2.sql import SQL, Identifier
from ..exceptions import ConnectionException
from .__interface import IConnection
from .__alias import T, WhereType, IdType


class Postgres(IConnection):
    _client: Union[connection, None] = None

    @property
    def client(self) -> connection:
        if self._client is None:
            raise ConnectionException('Connection is not set')
        return super().client

    def _is_connected(self) -> bool:
        if self._client is None:
            return False
        _status: int = self._client.status
        return _status > 0

    def connect(self) -> None:
        _port: Union[int, None] = None
        try:
            if (_port := self._settings.get_int('conn.postgres.port')) is None:
                _port = 5432
        except KeyError:
            _port = 5432

        _user: Union[str, None] = None
        _pwd: Union[str, None] = None

        try:
            _user = self._settings.get('conn.postgres.user')
        except KeyError:
            pass

        try:
            _pwd = self._settings.get('conn.postgres.password')
        except KeyError:
            pass

        _data: Dict[str, Union[str, int, None]] = {
            'host': self._settings.get_ns('conn.postgres.host'),
            'port': _port,
            'database': self._settings.get_ns('conn.postgres.db'),
            'user': _user,
            'password': _pwd,
        }
        self._client = connect(**_data)

    def close(self) -> None:
        if self._client is None:
            return
        self._client.close()
        self._client = None

    def insert(self, obj: T) -> Tuple[Union[T, None], IdType, bool]:
        return super().insert(obj)

    def update(self, obj: T, /, id: IdType = None, where: WhereType = None) -> Tuple[Union[T, None], bool]:
        return super().update(obj, id, where)

    def select(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> Iterator[T]:
        _fields: List[Identifier] = []
        _fields_str: List[str] = list([fld for fld, _ in t.get_fields()])
        _fields_str.sort()
        _fields = list([Identifier(x) for x in _fields_str])
        del _fields_str
        return super().select(t, id, where)

    def delete_where(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> int:
        return super().delete_where(t, id, where)

    def create_table(self, t: Type[T]) -> bool:
        return super().create_table(t)

    def drop_table(self, t: Type[T]) -> bool:
        return super().drop_table(t)
