# pylint: disable=invalid-name,missing-function-docstring,missing-class-docstring,missing-module-docstring,suppressed-message,locally-disabled

from abc import ABC
from re import Pattern
from bson import ObjectId
from datetime import date, datetime, time
from typing import Any, Dict, Generic, List, Tuple, TypeVar, Union, Type, Iterable
from enum import Enum, auto
from dataclasses import dataclass

# Enums


class QueryComparison(Enum):
    Eq = auto()         # equal
    Gt = auto()         # greater than
    Gte = auto()        # greater than or equal
    Lt = auto()         # less than
    Lte = auto()        # less than or equal
    Ne = auto()         # not equal
    In = auto()         # in
    NotIn = auto()      # not in
    Like = auto()       # like
    NotLike = auto()    # not like
    IsNull = auto()     # is null
    IsNotNull = auto()  # is not null
    Between = auto()    # between
    Outside = auto()    # not between


class QueryJoin(Enum):
    And = auto()
    Or = auto()
    Not = auto()
    AndNot = auto()
    OrNot = auto()
    Init = auto()


class QueryAction(Enum):
    Create = auto()
    Select = auto()
    Insert = auto()
    Update = auto()
    Delete = auto()


T = TypeVar('T', bound=Any)


@dataclass
class QueryCondition:
    data_type: str
    data_value: Union[
        int,
        str,
        float,
        date,
        datetime,
        time,
        bool,
        None,
        Pattern,
        ObjectId,
        Tuple[int, int],
        Tuple[float, float],
        Tuple[date, date],
        Tuple[datetime, datetime],
        Tuple[time, time],
        List[int],
        List[float],
        List[str],
        List[date],
        List[datetime],
        List[time]]
    comparison: QueryComparison
    comparison_join: QueryJoin


class QueryWhere:
    _query: 'IQuery'

    def __init__(self, query: 'IQuery') -> None:
        self._query = query

    def Where(self, field: str, comparison: str, value: str) -> 'QueryWhere':
        return self

    def And(self, field: str, comparison: str, value: str) -> 'QueryWhere':
        return self

    def Or(self, field: str, comparison: str, value: str) -> 'QueryWhere':
        return self

    def Group(self, conditions: List['QueryWhere']) -> 'QueryWhere':
        return self

    def NotGroup(self, conditions: List['QueryWhere']) -> 'QueryWhere':
        return self

    def AndGroup(self, conditions: List['QueryWhere']) -> 'QueryWhere':
        return self

    def OrGroup(self, conditions: List['QueryWhere']) -> 'QueryWhere':
        return self

    def AndNotGroup(self, conditions: List['QueryWhere']) -> 'QueryWhere':
        return self

    def OrNotGroup(self, conditions: List['QueryWhere']) -> 'QueryWhere':
        return self

    @property
    def EndWhere(self) -> 'IQuery':
        return self._query

    @property
    def All(self) -> 'IQuery':
        return self._query


class IQuery(ABC, Generic[T]):
    _action: QueryAction
    _t: Type[T]
    _where: List[QueryCondition]

    def Where(self, where: QueryCondition) -> 'IQuery[T]':
        self._where.append(where)
        return self

    def __init__(self, t: Type[T]) -> None:
        self._t = t
        self._where = []
        self._action = QueryAction.Select

    @classmethod
    def parse(cls, query: str, t: Union[Type[T], T]) -> 'IQuery[T]':
        _query: 'IQuery[T]'
        if isinstance(t, type):
            _query = cls(t)
        else:
            _query = cls(type(t))
        return _query

    @property
    def Select(self) -> QueryWhere:
        self._action = QueryAction.Select
        return QueryWhere(self)

    def Update(self, obj: T, fields: Union[str, Iterable[str]]) -> QueryWhere:
        self._action = QueryAction.Update
        return QueryWhere(self)

    def Insert(self, obj: T) -> 'IQuery[T]':
        self._action = QueryAction.Insert
        return self

    @property
    def Delete(self) -> QueryWhere:
        self._action = QueryAction.Delete
        return QueryWhere(self)

    def CreateTable(self) -> 'IQuery[T]':
        self._action = QueryAction.Create
        return self

    def _validate(self) -> None:
        if self._action is QueryAction.Create or self._action is QueryAction.Insert and len(self._where) > 0:
            raise ValueError()

    def convert(self) -> Tuple[Union[str, None], Union[Dict[str, Any], None]]:
        self._validate()
        return ('', {})
