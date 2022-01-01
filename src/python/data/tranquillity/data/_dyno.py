from typing import Any, Dict, Iterable, Type
from .__interface import IDBObject
from ._dataclasses import DataTable, DataField


def dynamic(n: str, table: DataTable, fields: Iterable[DataField]) -> Type[IDBObject]:
    props: Dict[str, Any] = {}
    props['__table__'] = table
    props['__fields__'] = tuple(list(fields).copy())
    out: Type[IDBObject] = type(n, (IDBObject,), props)
    return out
