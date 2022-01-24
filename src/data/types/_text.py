from ast import Call
from typing import Union, Callable
from re import Pattern
from ._dtype import DType
from ._nsdtype import NSDType


class Text(DType[str]):
    _t = str
    _not_empty: bool = False
    _match: Union[Pattern, None] = None
    _transform: Union[Callable[[str], str], None] = None

    def __init__(self, field: Union[str, None] = None, value: Union[str, None] = None, is_id: bool = False, required: bool = True, default: Union[str, None] = None, nullable: bool = True, json_field: Union[str, None] = None) -> None:
        super().__init__(field, value, is_id, required, default, nullable, json_field)


class NSText(NSDType[str]):
    _t = str

    def __init__(self, field: Union[str, None] = None, value: Union[str, None] = None, is_id: bool = False, required: bool = True, default: Union[str, None] = None, json_field: Union[str, None] = None) -> None:
        super().__init__(field, value, is_id, required, default, json_field)


class String(Text):
    pass


class NSString(NSText):
    pass
