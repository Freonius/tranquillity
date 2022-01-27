from typing import Any
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
