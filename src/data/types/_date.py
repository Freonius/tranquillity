from datetime import date
from typing import Union, Any
from pendulum import parse
from graphene import DateTime as GqlDateTime, NonNull
from ._dtype import DType
from ._nsdtype import NSDType
from ._datetime import _convert


class DateTime(DType[date]):
    _t = date
    _format: str = '%Y-%m-%d'

    def iter_value(self) -> Union[str, None]:
        if self.value is None:
            return None
        return self.value.strftime(self._format)

    def _ggt(self) -> Any:
        return GqlDateTime

    def _value_setter(self, val: Union[date, None, str]) -> None:
        val = _convert(val)
        if val is not None:
            val = val.date()
        super()._value_setter(val)

    def __init__(self,
                 value: Union[date, str, None] = None,
                 *,
                 format: Union[str, None] = '%Y-%m-%d',
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[date, str, None] = None,
                 nullable: bool = True, json_field: Union[str, None] = None) -> None:
        value = _convert(value)
        if value is not None:
            value = value.date()
        default = _convert(default)
        if default is not None:
            default = default.date()
        if format is None:
            format = '%Y-%m-%d'
        self._format = format
        super().__init__(field, value, is_id, required, default, nullable, json_field)


class NSDate(NSDType[date]):
    _t = date
    _format: str = '%Y-%m-%d'

    def iter_value(self) -> Union[str, None]:
        if self.value is None:
            return None
        return self.value.strftime(self._format)

    def _ggt(self) -> Any:
        return lambda **kwargs: NonNull(GqlDateTime, **kwargs)

    def _value_setter(self, val: Union[date, None, str]) -> None:
        val = _convert(val)
        if val is not None:
            val = val.date()
        super()._value_setter(val)

    def __init__(self,
                 value: Union[date, str, None] = None,
                 *,
                 format: Union[str, None] = '%Y-%m-%d',
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[date, str, None] = None,
                 json_field: Union[str, None] = None) -> None:
        value = _convert(value)
        if value is not None:
            value = value.date()
        default = _convert(default)
        if default is not None:
            default = default.date()
        if format is None:
            format = '%Y-%m-%d'
        self._format = format
        super().__init__(field, value, is_id, required, default, json_field)
