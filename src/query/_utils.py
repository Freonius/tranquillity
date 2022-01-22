from datetime import date, datetime, time
from typing import Union
from ._enums import SqlDialect
from ._dataclasses import Table


def _date2sql(dt: Union[date, datetime, time], dialect: SqlDialect) -> str:
    if isinstance(dt, date):
        raise NotImplementedError
    if isinstance(dt, datetime):
        raise NotImplementedError
    if isinstance(dt, time):
        raise NotImplementedError


def _val2sql(val: Union[None, str, date, datetime, time, int, float], dialect: SqlDialect) -> str:
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
