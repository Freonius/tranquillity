from datetime import datetime, time
from typing import Union, Any
from pendulum import parse
from graphene import NonNull, Time as GqlTime
from sqlalchemy import Column, Time as SqlTime
from ._dtype import DType
from ._nsdtype import NSDType


def _convert(val: Union[datetime, None, str, time]) -> Union[time, None]:
    if isinstance(val, datetime):
        return val.time()
    elif isinstance(val, str):
        if isinstance(_new_val := parse(val, strict=False), datetime):
            if isinstance((val := _new_val.time()), time):
                return val
            return None
        else:
            raise TypeError
    else:
        return val


class Time(DType[time]):
    _t = time
    _format: str = 'H:%M:%S.%f'

    def iter_value(self) -> Union[str, None]:
        if self.value is None:
            return None
        return self.value.strftime(self._format)

    def _ggt(self) -> Any:
        return GqlTime

    def _value_setter(self, val: Union[datetime, None, str, time]) -> None:
        super()._value_setter(_convert(val))

    def __init__(self,
                 value: Union[time, str, None, datetime] = None,
                 *,
                 format: Union[str, None] = '%H:%M:%S.%f',
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[time, str, None, datetime] = None,
                 nullable: bool = True, json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False,) -> None:
        value = _convert(value)
        default = _convert(default)
        if format is None:
            format = 'H:%M:%S.%f'
        self._format = format
        super().__init__(field, value, is_id, required, default,
                         nullable, json_field, indexable, filterable, exclude)

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, SqlTime,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )


class NSTime(NSDType[time]):
    _t = time
    _format: str = '%H:%M:%S.%f'

    def iter_value(self) -> Union[str, None]:
        if self.value is None:
            return None
        return self.value.strftime(self._format)

    def _ggt(self) -> Any:
        return lambda **kwargs: NonNull(GqlTime, **kwargs)

    def _value_setter(self, val: Union[datetime, None, str, time]) -> None:
        super()._value_setter(_convert(val))

    def __init__(self,
                 value: Union[datetime, time, str, None] = None,
                 *,
                 format: Union[str, None] = '%H:%M:%S.%f',
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[datetime, time, str, None] = None,
                 json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False,) -> None:
        value = _convert(value)
        default = _convert(default)
        if format is None:
            format = '%H:%M:%S.%f'
        self._format = format
        super().__init__(field, value, is_id, required, default,
                         json_field, indexable, filterable, exclude)

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, SqlTime,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )
