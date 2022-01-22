from typing import TYPE_CHECKING
from ._enums import QueryComparison, QueryJoin, QueryType
from ._values import QWhereV, QWhereVR

if TYPE_CHECKING:
    from ._query import Q_


class QSelect:
    _parent: 'Q_'

    def __init__(self, parent: 'Q_') -> None:
        self._parent = parent

    def AndWhere(self, field: str) -> 'QWhereS':
        self._parent._add_where_bit(QueryJoin.And)
        return QWhereS(self, field)

    def OrWhere(self, field: str) -> 'QWhereS':
        self._parent._add_where_bit(QueryJoin.Or)
        return QWhereS(self, field)

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
