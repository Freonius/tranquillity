from typing import Any, Union
from graphene import Boolean, NonNull
from sqlalchemy import Column, Boolean as SqlBoolean
from ._dtype import DType
from ._nsdtype import NSDType


class Bool(DType[bool]):
    _t = bool

    def _ggt(self) -> Any:
        return Boolean

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, SqlBoolean,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )

    def __init__(self,
                 value: Union[bool, None] = None,
                 *,
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[bool, None] = None,
                 nullable: bool = True,
                 json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False) -> None:
        super().__init__(field, value, is_id, required, default,
                         nullable, json_field, indexable, filterable, exclude)


class NSBool(NSDType[bool]):
    _t = bool

    def _ggt(self) -> Any:
        return lambda **kwargs: NonNull(Boolean, **kwargs)

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, SqlBoolean,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )

    def __init__(self,
                 value: Union[bool, None] = None,
                 *,
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[bool, None] = None,
                 json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False) -> None:
        super().__init__(field, value, is_id, required, default,
                         json_field, indexable, filterable, exclude)
