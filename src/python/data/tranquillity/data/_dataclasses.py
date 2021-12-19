from datetime import date, datetime, time
from dataclasses import dataclass
from typing import Union, Iterable, Callable, Any, Tuple
from ._types import DataType
from ..api._dataclasses import Role, ApiAddr


@dataclass
class DataTable:
    table: str
    schema: Union[str, None] = None
    db: Union[str, None] = None


@dataclass
class DataField:
    column_name: str
    column_type: DataType
    is_nullable: bool = True
    default: Union[
        int,
        str,
        float,
        date,
        datetime,
        time,
        bool,
        None] = None
    required: bool = True
    subobject_structure: Union[Iterable['DataField'], None] = None
    missing: Union[
        int,
        str,
        float,
        date,
        datetime,
        time,
        bool,
        None] = None
    pre_load: Union[None, Callable[[Any], Any]] = None
    pre_check: Union[None, Callable[[Any], None]] = None
    check: Union[None, Callable[[Any], None]] = None
    serialize_only: bool = False
    serialize_fun: Union[None, Callable[[Any], Any]] = None
    primary_key: bool = False
    auto_increment: bool = False
    ref: Union[None, Tuple[DataTable, 'DataField'],
               Tuple[ApiAddr, str]] = None
    role_can_write: Iterable[Role] = [Role.ADMIN, Role.USER]
    role_can_read: Iterable[Role] = [Role.ADMIN, Role.USER, Role.NOT_LOGGED]
