from typing import Any, Dict, Iterable, List, Tuple, Union
from datetime import datetime
from abc import ABC, abstractmethod
from pymongo.collection import ObjectId
from marshmallow import Schema
from flask import request
from ..connections.__interface import IConnection
from ..query.__interface import IQuery
from ._dataclasses import DataTable, DataField


class IDBObject(ABC):
    _data: Dict[str, Any] = {}
    _schema: Schema
    __table__: DataTable
    __fields__: Iterable[DataField]

    def __init__(self, data: Dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise TypeError(f'data must be of type dict, got {type(data)}')
        self._data = data
        self._check_required()
        self._pre_check()

    def _check_required(self) -> None:
        pass

    def _pre_check(self) -> None:
        for field in self.__fields__:
            if field.pre_load is not None:
                self._data[field.column_name] = field.pre_load(
                    self._data[field.column_name])
            if field.pre_check is not None:
                field.pre_check(self._data[field.column_name])

    @classmethod
    def _define(cls) -> Iterable[DataField]:
        return cls.__fields__

    @classmethod
    def _table(cls) -> DataTable:
        return cls.__table__

    # pylint: disable=invalid-name
    @property
    def id(self) -> Union[int, str, ObjectId, None]:
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
    def from_body(cls) -> 'IDBObject':
        body: Dict[str, Any] = {}
        if request.is_json:
            tmp = request.get_json()
            if isinstance(tmp, dict):
                body = tmp
        out: 'IDBObject' = cls(body)
        return out

    @classmethod
    def get(cls, conn: IConnection, query: Union[IQuery, None] = None) -> Union['IDBObject', List['IDBObject'], None]:
        raise NotImplementedError()

    def add(self) -> bool:
        raise NotImplementedError()

    def update(self) -> bool:
        if self.id is None:
            raise ValueError
        raise NotImplementedError()

    def delete(self) -> bool:
        raise NotImplementedError()

    def serialize(self) -> Dict[str, Any]:
        tmp: Union[List[Dict[str, Any]], Dict[str, Any],
                   None] = self._schema.load(self._data, many=False)
        if isinstance(tmp, dict):
            return tmp
        raise ValueError

    def json(self) -> Dict[str, Any]:
        return self.serialize()

    @property
    def is_serializable(self) -> bool:
        raise NotImplementedError()

    def __getitem__(self, key: str) -> Any:
        if key in self._data.keys():
            return self._data[key]
        return None

    def __setitem__(self, key: str, val: Any) -> None:
        self._data[key] = val
