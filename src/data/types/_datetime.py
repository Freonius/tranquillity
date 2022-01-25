from datetime import datetime
from typing import Union, List, Dict, Any
from pendulum.datetime import DateTime as PDateTime
from pendulum import parse
from graphene import DateTime as GqlDateTime, NonNull
from ._dtype import DType
from ._nsdtype import NSDType


class DateTime(DType[datetime]):
    _t = datetime
    _format: str = '%Y-%m-%d %H:%M:%S.%f'

    def iter_value(self) -> Union[str, None]:
        if self.value is None:
            return None
        return self.value.strftime(self._format)

    def _ggt(self) -> Any:
        return GqlDateTime

    def _value_setter(self, val: Union[datetime, None, str]) -> None:
        if isinstance(val, datetime):
            super()._value_setter(val)
        elif isinstance(val, str):
            if isinstance(_new_val := parse(val, strict=False), datetime):
                super()._value_setter(_new_val)
            else:
                raise TypeError
        else:
            super()._value_setter(val)

    def __init__(self,
                 value: Union[datetime, str, None] = None,
                 *,
                 format: Union[str, None] = '%Y-%m-%d %H:%M:%S.%f',
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[datetime, str, None] = None,
                 nullable: bool = True, json_field: Union[str, None] = None) -> None:
        if isinstance(value, str):
            if isinstance(_new_val := parse(value, strict=False), datetime):
                value = _new_val
            else:
                raise TypeError
        if isinstance(default, str):
            if isinstance(_new_default := parse(default, strict=False), datetime):
                default = _new_default
            else:
                raise TypeError
        if format is None:
            format = '%Y-%m-%d %H:%M:%S.%f'
        self._format = format
        super().__init__(field, value, is_id, required, default, nullable, json_field)


class NSDateTime(NSDType[datetime]):
    _t = datetime
    _format: str = '%Y-%m-%d %H:%M:%S.%f'

    def iter_value(self) -> Union[str, None]:
        if self.value is None:
            return None
        return self.value.strftime(self._format)

    def _ggt(self) -> Any:
        return GqlDateTime

    def _value_setter(self, val: Union[datetime, None, str]) -> None:
        if isinstance(val, datetime):
            super()._value_setter(val)
        elif isinstance(val, str):
            if isinstance(_new_val := parse(val, strict=False), datetime):
                super()._value_setter(_new_val)
            else:
                raise TypeError
        else:
            super()._value_setter(val)

    def __init__(self,
                 value: Union[datetime, str, None] = None,
                 *,
                 format: Union[str, None] = '%Y-%m-%d %H:%M:%S.%f',
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[datetime, str, None] = None,
                 json_field: Union[str, None] = None) -> None:
        if isinstance(value, str):
            if isinstance(_new_val := parse(value, strict=False), datetime):
                value = _new_val
            else:
                raise TypeError
        if isinstance(default, str):
            if isinstance(_new_default := parse(default, strict=False), datetime):
                default = _new_default
            else:
                raise TypeError
        if format is None:
            format = '%Y-%m-%d %H:%M:%S.%f'
        self._format = format
        super().__init__(field, value, is_id, required, default, json_field)
