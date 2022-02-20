from typing import Union, Any, Iterator, List, Dict, Type, Tuple
from boto3 import resource
import boto3
from ..__interface import IConnection
from ..__alias import T, IdType, WhereType

import boto3.resources.response as db


class DynamoDB(IConnection):
    def connect(self) -> None:
        return super().connect()

    def close(self) -> None:
        return super().close()

    @property
    def client(self) -> Any:
        return super().client

    def _is_connected(self) -> bool:
        return super()._is_connected()

    def create_table(self, t: Type[T]) -> bool:
        return super().create_table(t)

    def drop_table(self, t: Type[T]) -> bool:
        return super().drop_table(t)

    def insert(self, obj: T) -> Tuple[Union[T, None], IdType, bool]:
        return super().insert(obj)

    def select(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> Iterator[T]:
        return super().select(t, id, where)

    def update(self, obj: T, /, id: IdType = None, where: WhereType = None) -> Tuple[Union[T, None], bool]:
        return super().update(obj, id, where)

    def delete_where(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> int:
        return super().delete_where(t, id, where)
