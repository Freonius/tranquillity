from typing import Any, Dict, Generic, List, Tuple, Type, TypeVar, Union, get_args
from datetime import datetime
from abc import ABC, abstractmethod
from pymongo.collection import ObjectId
from marshmallow import Schema
from ._connection import IConnection
from ._query import IQuery

# pylint: disable=invalid-name
T = TypeVar('T', bound=IConnection)
U = TypeVar('U', bound=Schema)
# pylint: enable=invalid-name

class IDBObject(ABC, Generic[T, U]):

    _data: Dict[str, Any] = {}

    @classmethod
    def __conn__(cls) -> Type[T]:
        # pylint: disable=no-member
        return get_args(cls.__orig_bases__[0])[0]
        # pylint: enable=no-member

    @classmethod
    def __schema__(cls) -> U:
        # pylint: disable=no-member
        return get_args(cls.__orig_bases__[0])[1]()
        # pylint: enable=no-member

    def __init__(self, data: Dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise TypeError(f'data must be of type dict, got {type(data)}')
        self._data = data
        self.__load__()

    @abstractmethod
    def __load__(self) -> None:
        pass

    # pylint: disable=invalid-name
    @property
    def id(self) -> Union[int, str, Tuple[Union[str, int, datetime], ...], ObjectId, None]:
        '''
        Object id.
        '''
        if 'id' in self._data.keys():
            return self._data['id']
        if '_id' in self._data.keys():
            return self._data['_id']
        return None
    # pylint: enable=invalid-name

    @classmethod
    def from_body(cls, key: Union[str, None] = None) -> 'IDBObject':
        c: 'IDBObject' = cls({})

    @classmethod
    def get(cls, query: Union[IQuery, None] = None, redis: Union[None,] = None) -> Union['IDBObject', List['IDBObject'], None]:
        conn: T
        conn_t: Type[T] = cls.__conn__()
        with conn_t() as conn:
            conn.is_connected

    def add(self) -> bool:
        pass

    def update(self) -> bool:
        pass

    def delete(self) -> bool:
        pass

    def serialize(self) -> Dict[str, Any]:
        pass

    def json(self) -> Dict[str, Any]:
        return self.serialize()

    @property
    def is_serializable(self) -> bool:
        pass

    def __getitem__(self, key: str) -> Any:
        if key in self._data.keys():
            return self._data[key]
        return None

    def __setitem__(self, key: str, val: Any) -> None:
        self._data[key] = val
