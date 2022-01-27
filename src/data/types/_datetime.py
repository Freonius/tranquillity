from datetime import datetime, date, time
from typing import Union, Any
from pendulum import parse
from pendulum.datetime import DateTime as PenDateTime
from graphene import DateTime as GqlDateTime, NonNull
from sqlalchemy import Column, DateTime as SqlDateTime
from ._dtype import DType
from ._nsdtype import NSDType


def _convert(value: Union[datetime, date, str, None]) -> Union[datetime, None]:
    if isinstance(value, str) and value.strip().lower() == 'today':
        value = date.today()
    if isinstance(value, str):
        if isinstance(_new_val := parse(value, strict=False), (datetime, date)):
            if not isinstance(_new_val, datetime):
                _new_val = PenDateTime.combine(
                    _new_val, time(0, 0))
                if not isinstance(_new_val, datetime):
                    raise TypeError
            value = _new_val
        else:
            raise TypeError
    if not isinstance(value, datetime) and value is not None:
        value = PenDateTime.combine(
            value, time(0, 0))
        if not isinstance(value, datetime):
            raise TypeError
    if isinstance(value, datetime):
        return value
    return None


class DateTime(DType[datetime]):
    _t = datetime
    _format: str = '%Y-%m-%dT%H:%M:%S.%f'

    def iter_value(self) -> Union[str, None]:
        if self.value is None:
            return None
        return self.value.strftime(self._format)

    def _ggt(self) -> Any:
        return GqlDateTime

    def _value_setter(self, val: Union[datetime, None, str]) -> None:
        val = _convert(val)
        super()._value_setter(val)

    def __init__(self,
                 value: Union[datetime, date, str, None] = None,
                 *,
                 format: Union[str, None] = '%Y-%m-%dT%H:%M:%S.%f',
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[datetime, str, None] = None,
                 nullable: bool = True, json_field: Union[str, None] = None) -> None:
        value = _convert(value)
        default = _convert(default)
        if format is None:
            format = '%Y-%m-%dT%H:%M:%S.%f'
        self._format = format
        super().__init__(field, value, is_id, required, default, nullable, json_field)

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, SqlDateTime,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )


class NSDateTime(NSDType[datetime]):
    _t = datetime
    _format: str = '%Y-%m-%dT%H:%M:%S.%f'

    def iter_value(self) -> Union[str, None]:
        if self.value is None:
            return None
        return self.value.strftime(self._format)

    def _ggt(self) -> Any:
        return lambda **kwargs: NonNull(GqlDateTime, **kwargs)

    def _value_setter(self, val: Union[datetime, None, str, date]) -> None:
        val = _convert(val)
        super()._value_setter(val)

    def __init__(self,
                 value: Union[datetime, str, None] = None,
                 *,
                 format: Union[str, None] = '%Y-%m-%dT%H:%M:%S.%f',
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
            format = '%Y-%m-%dT%H:%M:%S.%f'
        self._format = format
        super().__init__(field, value, is_id, required, default, json_field)

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, SqlDateTime,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )
