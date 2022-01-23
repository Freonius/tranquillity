from typing import Union
from ._dtype import DType


class Text(DType[str]):

    def __init__(self,
                 field: str,
                 value: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[str, None] = None,
                 nullable: bool = True,
                 json_field: Union[str, None] = None) -> None:
        self._field = field
        self._is_id = is_id
        self._value = value
        self._required = required
        self._default = default
        self._nullable = nullable
        self._json_field = json_field


class String(Text):
    pass
