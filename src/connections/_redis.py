from typing import Any, Dict, Type, Tuple, Union, Iterator
from redis import Redis as RedisClient
from ..exceptions import ConnectionException
from .__interface import IConnection
from .__alias import T, WhereType, IdType


class Redis(IConnection):
    _client: Union[None, RedisClient]

    @property
    def client(self) -> RedisClient:
        if self._client is None:
            raise ConnectionException('client is not set')
        return self._client

    def _is_connected(self) -> bool:
        if self._client is None:
            return False
        return self._client.ping()

    def connect(self) -> None:
        return super().connect()

    def close(self) -> None:
        if self._client is None:
            return
        self._client.close()
        self._client = None

    def insert(self, obj: T) -> Tuple[Union[T, None], IdType, bool]:
        _key: str = obj.__class__.__name__.lower()
        if (_id := obj.get_id()) is not None:
            _key += f'/{str(_id)}'
            del _id
        _data: Union[str, Dict[str, Any]] = obj.to_json()
        if isinstance(_data, dict):
            raise TypeError
        _success: Union[bool, None] = self.client.set(
            _key, value=_data, ex=18000)
        if _success is None:
            _success = False
        return obj, obj.get_id(), _success

    def select(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> Iterator[T]:
        return super().select(t, id, where)

    def delete_where(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> int:
        return super().delete_where(t, id, where)

    def update(self, obj: T, /, id: IdType = None, where: WhereType = None) -> Tuple[Union[T, None], bool]:
        return super().update(obj, id, where)

    def create_table(self, t: Type[T]) -> bool:
        return super().create_table(t)

    def drop_table(self, t: Type[T]) -> bool:
        return super().drop_table(t)
