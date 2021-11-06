from typing import Any, Dict, Iterable, Type
from .__interface import IDBObject
from ._dataclasses import DataTable, DataField, DataType


def dynamic(n: str, table: DataTable, fields: Iterable[DataField]) -> Type[IDBObject]:
    props: Dict[str, Any] = {}
    props['__table__'] = table
    props['__fields__'] = tuple(list(fields).copy())
    out = type(n, (IDBObject,), props)
    return out
