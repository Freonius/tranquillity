from datetime import date, datetime, time
from typing import Type, Union
from bson import ObjectId
from ._enums import SqlDialect, QueryType
from ._dataclasses import Table


def type_to_querytype(t: Type, is_list: bool = False) -> QueryType:
    if is_list is True:
        return QueryType.List
    if t is str:
        return QueryType.String
    if t is int:
        return QueryType.Int
    if t is float:
        return QueryType.Float
    if t is bool:
        return QueryType.Bool
    if t is date:
        return QueryType.Date
    if t is time:
        return QueryType.Time
    if t is datetime:
        return QueryType.DateTime
    if t is ObjectId:
        return QueryType.MongoId
    return QueryType.Object


def _date2sql(dt: Union[date, datetime, time], dialect: SqlDialect) -> str:
    if isinstance(dt, date):
        raise NotImplementedError
    if isinstance(dt, datetime):
        raise NotImplementedError
    if isinstance(dt, time):
        raise NotImplementedError


def _val2sql(val: Union[None, str, date, datetime, time, int, float, object], dialect: SqlDialect) -> str:
    if val is None:
        return ''
    if isinstance(val, (float, int, str)):
        return str(val)
    if isinstance(val, (date, datetime, time)):
        return _date2sql(val, dialect)
    else:
        raise TypeError


def _fld2sql(fld: str, dialect: SqlDialect) -> str:
    raise NotImplementedError


def _tbl2sql(tbl: Table, dialect: SqlDialect) -> str:
    raise NotImplementedError


def _t2esm(t: Type) -> str:
    if t is str:
        return 'text'
    if t is int:
        return 'integer'
    if t is float:
        return 'float'
    if t is datetime:
        return 'datetime'
    return 'object'
