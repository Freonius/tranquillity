from typing import Any, Union, Iterable, Tuple
from sqlalchemy import Column, Integer as SqlInt
from bson import ObjectId
from graphene.types import String
from ._dtype import DType
from ._int import Int
from ._text import String as DString


class Id(Int):
    _auto_increment: bool = True

    def __init__(self,
                 value: Union[int, None] = None,
                 field: Union[str, None] = None, *,
                 auto_increment: bool = True,
                 required: bool = True, json_field: Union[str, None] = None,
                 between: Union[Tuple[int, int], None] = None,
                 is_in: Union[None, Iterable[int]] = None, exclude: bool = False) -> None:
        self._auto_increment = auto_increment
        super().__init__(value, field, is_id=True, required=required, default=None, nullable=True,
                         json_field=json_field, greater_than_zero=True,
                         greater_then_or_equal_to_zero=False, between=between, is_in=is_in, exclude=exclude)

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, SqlInt,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
            autoincrement=self._auto_increment,
        )


class MongoId(DType[ObjectId]):
    _t = ObjectId

    def _value_setter(self, val: Union[ObjectId, str, None]) -> None:
        if isinstance(val, str):
            val = ObjectId(val)
        return super()._value_setter(val)

    def iter_value(self) -> Union[str, None]:
        if self._value is None:
            if self._default is not None:
                return str(self._default)
            return None
        return str(self._value)

    def __init__(self,
                 value: Union[ObjectId, str, None] = None,
                 field: Union[str, None] = '_id',
                 is_id: bool = True,
                 required: bool = True,
                 generate: bool = False,
                 json_field: Union[str, None] = None, exclude: bool = False) -> None:
        default: Union[ObjectId, None] = None
        if generate:
            default = ObjectId()
        super().__init__(field, value, is_id, required,
                         default, True, json_field, True, True, exclude)

    def _ggt(self) -> Any:
        return String

    def get_sqlalchemy_column(self) -> Column:
        raise TypeError('mongoid cannot be converted to sqlalchemy')


class StrId(DString):
    def __init__(self,
                 value: Union[str, None] = None,
                 field: Union[str, None] = '_id',
                 default: Union[str, None] = None,
                 json_field: Union[str, None] = '_id',
                 exclude: bool = False,) -> None:
        super().__init__(value=value, field=field, primary_key=True,
                         required=True, default=default, nullable=True,
                         json_field=json_field, not_empty=True, auto_strip=True,
                         indexable=True, filterable=True, exclude=exclude)

    def serialize(self) -> Union[str, None]:
        return self._value
