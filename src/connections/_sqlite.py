from typing import Type, Tuple, Iterator, List, Union, Dict
from sqlite3 import Connection, connect, Cursor
from ..exceptions import ConnectionException
from .__interface import IConnection
from .__alias import T, WhereType, IdType


class Sqlite(IConnection):
    _client: Union[Connection, None] = None

    def connect(self) -> None:
        return super().connect()

    def _is_connected(self) -> bool:
        return super()._is_connected()

    @property
    def client(self) -> Connection:
        if self._client is None:
            raise ConnectionException
        return self._client

    def close(self) -> None:
        if self._client is None:
            return
        self._client.close()
        self._client = None

    def insert(self, obj: T) -> Tuple[Union[T, None], IdType, bool]:
        _crs: Cursor = self.client.execute('')
        _id: Union[int, str, None] = None
        _success: bool = _crs.rowcount == 1
        if not isinstance((_id := _crs.lastrowid), (int, str)):
            _id = None
        _crs.close()
        if _id is not None:
            obj.set_id(_id)
        return obj, _id, _success

    def select(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> Iterator[T]:
        return super().select(t, id, where)

    def update(self, obj: T, /, id: IdType = None, where: WhereType = None) -> Tuple[Union[T, None], bool]:
        return super().update(obj, id, where)

    def delete_where(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> int:
        return super().delete_where(t, id, where)

    def create_table(self, t: Type[T]) -> bool:
        return super().create_table(t)

    def drop_table(self, t: Type[T]) -> bool:
        return super().drop_table(t)
