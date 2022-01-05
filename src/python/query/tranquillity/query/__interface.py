# pylint: disable=invalid-name,missing-function-docstring,missing-class-docstring,missing-module-docstring,suppressed-message,locally-disabled

from datetime import date, datetime, time
from typing import Any, Dict, List, Tuple, Union
from enum import Enum, auto
from dataclasses import dataclass

# Enums


class QueryFormatError(Exception):
    pass


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
    Close = auto()
    GroupInit = auto()
    GroupClose = auto()


class QueryAction(Enum):
    Create = auto()
    Select = auto()
    Insert = auto()
    Update = auto()
    Delete = auto()


class QueryType(Enum):
    String = auto()
    Int = auto()
    Float = auto()
    Num = auto()
    Date = auto()
    DateTime = auto()
    Time = auto()
    Uuid = auto()
    Id = auto()
    Object = auto()
    Bool = auto()
    List = auto()
    MongoId = auto()


class QWhereV:
    _val: Union[None, str, date, datetime, time, int, float]

    def __init__(self, val: Union[None, str, date, datetime, time, int, float]) -> None:
        self._val = val
        pass


class QWhereVR:
    _val: Tuple[Union[None, str, date, datetime, time, int, float], ...]

    def __init__(self, min_val, max_val) -> None:
        self._val = (min_val, max_val)
        pass


@dataclass
class WhereCondition:
    join: QueryJoin
    field: str
    type: QueryType
    comparison: QueryComparison
    value: Union[QWhereV, QWhereVR]


class Q_:
    _where: List[Union[QueryJoin, str, QueryType,
                       QWhereV, QWhereVR, QueryComparison]]
    _action: QueryAction
    _table: str
    _schema: Union[str, None]
    _fields: Union[List[str], None]
    _data: Union[Dict[str, Any], None]

    def __init__(self, action: QueryAction) -> None:
        self._action = action
        self._where = []

    def _add_where_bit(self, bit: Union[QueryJoin, str, QueryType,
                       QWhereV, QWhereVR, QueryComparison]) -> None:
        self._where.append(bit)

    @staticmethod
    def Select(*fields: str, from_table: str, with_schema: Union[str, None] = None) -> 'QSelect':
        return QSelect(Q_(QueryAction.Select))

    @staticmethod
    def Insert(data: Dict[str, Any], into_table: str, with_schema: Union[str, None] = None) -> None:
        pass

    @staticmethod
    def Update(data: Dict[str, Any], from_table: str, with_schema: Union[str, None] = None) -> None:
        pass

    @staticmethod
    def Delete(from_table: str, with_schema: Union[str, None] = None) -> None:
        pass

    @staticmethod
    def Create(table: str, with_schema: Union[str, None] = None) -> None:
        pass


class QSelect:
    _parent: Q_

    def __init__(self, parent: Q_) -> None:
        if not isinstance(parent, Q_):
            raise QueryFormatError
        self._parent = parent

    @property
    def And(self) -> 'QSelect':
        self._parent._add_where_bit(QueryJoin.And)
        return self

    @property
    def Or(self) -> 'QSelect':
        self._parent._add_where_bit(QueryJoin.Or)
        return self

    def Where(self, field: str) -> 'QWhereS':
        self._parent._add_where_bit(QueryJoin.Init)
        return QWhereS(self, field)

    @property
    def Group(self) -> 'QSelect':
        self._parent._add_where_bit(QueryJoin.GroupInit)
        return self

    @property
    def EndGroup(self) -> 'QSelect':
        self._parent._add_where_bit(QueryJoin.GroupClose)
        return self


class QWhereS:
    _parent: QSelect

    def __init__(self, parent: QSelect, field: str) -> None:
        self._parent = parent
        self._parent._parent._add_where_bit(field)

    @property
    def WhichIsA(self) -> 'QWhereSAs':
        return QWhereSAs(self)


class QWhereSAs:
    _parent: QWhereS

    def __init__(self, parent: QWhereS) -> None:
        self._parent = parent

    @property
    def Int(self) -> 'QWhereSIs':
        self._parent._parent._parent._add_where_bit(QueryType.Int)
        return QWhereSIs(self)

    @property
    def String(self) -> 'QWhereSIs':
        self._parent._parent._parent._add_where_bit(QueryType.String)
        return QWhereSIs(self)

    @property
    def Float(self) -> 'QWhereSIs':
        self._parent._parent._parent._add_where_bit(QueryType.Float)
        return QWhereSIs(self)

    @property
    def Date(self) -> 'QWhereSIs':
        self._parent._parent._parent._add_where_bit(QueryType.Date)
        return QWhereSIs(self)

    @property
    def DateTime(self) -> 'QWhereSIs':
        self._parent._parent._parent._add_where_bit(QueryType.DateTime)
        return QWhereSIs(self)

    @property
    def Time(self) -> 'QWhereSIs':
        self._parent._parent._parent._add_where_bit(QueryType.Time)
        return QWhereSIs(self)

    @property
    def MongoId(self) -> 'QWhereSIs':
        self._parent._parent._parent._add_where_bit(QueryType.MongoId)
        return QWhereSIs(self)

    @property
    def Bool(self) -> 'QWhereSIs':
        self._parent._parent._parent._add_where_bit(QueryType.Bool)
        return QWhereSIs(self)


class QWhereSIs:
    _parent: QWhereSAs

    def __init__(self, parent: QWhereSAs) -> None:
        self._parent = parent

    def IsEqualTo(self, val) -> QSelect:
        self._parent._parent._parent._parent._add_where_bit(QueryComparison.Eq)
        self._parent._parent._parent._parent._add_where_bit(QWhereV(val))
        self._parent._parent._parent._parent._add_where_bit(QueryJoin.Close)
        return self._parent._parent._parent

    def IsLike(self, val) -> QSelect:
        self._parent._parent._parent._parent._add_where_bit(
            QueryComparison.Like)
        self._parent._parent._parent._parent._add_where_bit(QWhereV(val))
        self._parent._parent._parent._parent._add_where_bit(QueryJoin.Close)
        return self._parent._parent._parent

    def IsNotEqualTo(self, val) -> QSelect:
        self._parent._parent._parent._parent._add_where_bit(QueryComparison.Ne)
        self._parent._parent._parent._parent._add_where_bit(QWhereV(val))
        self._parent._parent._parent._parent._add_where_bit(QueryJoin.Close)
        return self._parent._parent._parent

    def IsGreaterThan(self, val) -> QSelect:
        self._parent._parent._parent._parent._add_where_bit(QueryComparison.Gt)
        self._parent._parent._parent._parent._add_where_bit(QWhereV(val))
        self._parent._parent._parent._parent._add_where_bit(QueryJoin.Close)
        return self._parent._parent._parent

    def IsGreaterThanOrEqualTo(self, val) -> QSelect:
        self._parent._parent._parent._parent._add_where_bit(
            QueryComparison.Gte)
        self._parent._parent._parent._parent._add_where_bit(QWhereV(val))
        self._parent._parent._parent._parent._add_where_bit(QueryJoin.Close)
        return self._parent._parent._parent

    def IsNull(self) -> QSelect:
        self._parent._parent._parent._parent._add_where_bit(
            QueryComparison.IsNull)
        self._parent._parent._parent._parent._add_where_bit(QWhereV(None))
        self._parent._parent._parent._parent._add_where_bit(QueryJoin.Close)
        return self._parent._parent._parent

    def IsNotNull(self) -> QSelect:
        self._parent._parent._parent._parent._add_where_bit(
            QueryComparison.IsNotNull)
        self._parent._parent._parent._parent._add_where_bit(QWhereV(None))
        self._parent._parent._parent._parent._add_where_bit(QueryJoin.Close)
        return self._parent._parent._parent

    def IsBetween(self, min_val, max_val) -> QSelect:
        self._parent._parent._parent._parent._add_where_bit(
            QueryComparison.Between)
        self._parent._parent._parent._parent._add_where_bit(
            QWhereVR(min_val=min_val, max_val=max_val))
        self._parent._parent._parent._parent._add_where_bit(QueryJoin.Close)
        return self._parent._parent._parent
