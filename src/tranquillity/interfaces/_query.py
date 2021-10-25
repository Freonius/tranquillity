# pylint: disable=invalid-name,missing-function-docstring,missing-class-docstring,missing-module-docstring,suppressed-message,locally-disabled

from abc import ABC
from typing import List, Tuple, Union, overload
from enum import Enum, auto
from multidispatch import multifunction

# Enums

class QueryComparisonEnum(Enum):
    Eq = auto()
    Gt = auto()
    Gte = auto()
    Lt = auto()
    Lte = auto()
    Not = auto()
    In = auto()
    Like = auto()
    IsNull = auto()
    Between = auto()

class QueryTypeEnum(Enum):
    String = auto()
    Int = auto()
    Float = auto()
    Number = auto()
    UInt = auto()
    Date = auto()
    DateTime = auto()
    Time = auto()
    Bool = auto()
    Id = auto()

class QueryJoinEnum(Enum):
    And = auto()
    Or = auto()

class QueryActionEnum(Enum):
    Create = auto()
    Read = auto()
    Insert = auto()
    Update = auto()
    Delete = auto()

class IQueryBit(ABC):
    _p: 'IQuery'

    def __init__(self, parent: 'IQuery') -> None:
        self._p = parent

class QueryComparison(IQueryBit):
    pass

class QueryField(IQueryBit):
    pass

class QueryType(IQueryBit):
    pass

class QueryAction(IQueryBit):
    @property
    def Read(self) -> None:
        pass

    @property
    def Create(self) -> None:
        pass

    @property
    def Delete(self) -> None:
        pass

    @property
    def Insert(self) -> None:
        pass

    @property
    def Update(self) -> None:
        pass

class QueryWhere(IQueryBit):
    def Where(self, field: str) -> 'QueryWhere':
        self._p._add()
        return self


class QueryFieldsContainer:
    _data: List[str]

    def __init__(self, *fields: List[str]) -> None:
        self._data = fields

    @property
    def Fields(self) -> List[str]:
        return self._data

class QueryTableContainer:
    _data: Tuple[Union[str, None], str]

    @multifunction(None, str)
    @overload
    def __init__(self, table: str) -> None:
        self._data = (None, table)

    @__init__.dispatch(None, str, str)
    @overload
    def __init__(self, schema: str, table: str) -> None:
        self._data = (schema, table)

    @property
    def Schema(self) -> Union[str, None]:
        return self._data[0]

    @property
    def Table(self) -> str:
        return self._data[1]

    @property
    def SchemaTable(self) -> str:
        if self._data[0] is None:
            return self._data[1]
        return self._data[0] + '.' + self._data[1]


class IQuery(ABC):
    _data: List[Union[QueryActionEnum, QueryFieldsContainer, QueryTableContainer]]
    def __init__(self) -> None:
        super().__init__()

    def Select(self, *fields: List[str]) -> 'IQuery':
        self._add(QueryActionEnum.Read)
        self._add(QueryFieldsContainer(fields))
        return self

    def _add(self, what) -> None:
        self._data.append(what)
