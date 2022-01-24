from typing import Union
from ._dtype import DType
from ._nsdtype import NSDType


class Float(DType[float]):
    _t = float

    def __init__(self, field: Union[str, None] = None, value: Union[float, None] = None, is_id: bool = False, required: bool = True, default: Union[float, None] = None, nullable: bool = True, json_field: Union[str, None] = None) -> None:
        super().__init__(field, value, is_id, required, default, nullable, json_field)


class NSFloat(NSDType[float]):
    _t = float

    def __init__(self, field: Union[str, None] = None, value: Union[float, None] = None, is_id: bool = False, required: bool = True, default: Union[float, None] = None, json_field: Union[str, None] = None) -> None:
        super().__init__(field, value, is_id, required, default, json_field)
