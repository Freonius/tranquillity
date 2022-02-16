from typing import Any, Iterator, Tuple, TypeVar, Generic, Type, Union, Dict as TDict
from sqlalchemy.types import JSON
from sqlalchemy import Column
from graphene import NonNull
from ._dtype import DType
from ._nsdtype import NSDType
from .._dataobject import DataObject
# TODO: sqlalchemy

T = TypeVar('T', bound=DataObject)


class Dict(DType[dict]):
    _t = dict
    _is_dict = True

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        if self._value is not None:
            for k, v in self._value:
                yield k, v

    def to_dict(self) -> TDict[str, Any]:
        if self._value is None:
            return {}
        return self._value

    def __init__(self, field: Union[str, None] = None, value: Union[TDict, None] = None, is_id: bool = False, required: bool = True, default: Union[TDict, None] = None, nullable: bool = True, json_field: Union[str, None] = None) -> None:
        super().__init__(field, value, is_id, required, default, nullable, json_field)

    def _ggt(self) -> Any:
        raise NotADirectoryError

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, JSON,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )


class NSDict(NSDType[dict]):
    _t = dict
    _is_dict = True

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        if self._value is not None:
            for k, v in self._value:
                yield k, v

    def to_dict(self) -> TDict[str, Any]:
        if self._value is None:
            return {}
        return self._value

    def __init__(self, field: Union[str, None] = None, value: Union[TDict, None] = None, is_id: bool = False, required: bool = True, default: Union[TDict, None] = None, json_field: Union[str, None] = None) -> None:
        super().__init__(field, value, is_id, required, default, json_field)

    def _ggt(self) -> Any:
        raise NotADirectoryError

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, JSON,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )


class Nested(DType[T], Generic[T]):
    _is_dict = True

    def __init__(self,
                 t: Type[T],
                 value: Union[T, None] = None,
                 *,
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[T, None] = None,
                 nullable: bool = True,
                 json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False,) -> None:
        self._t = t
        super().__init__(field, value, is_id, required, default,
                         nullable, json_field, indexable, filterable, exclude)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        if self._value is not None:
            for k, v in self._value.items():
                yield k, v

    def to_dict(self) -> TDict[str, Any]:
        if self._value is None:
            return {}
        return self._value.to_dict()

    def _ggt(self) -> Any:
        return self._t.to_graphql()

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, JSON,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )


class NSNested(NSDType[T], Generic[T]):
    _is_dict = True

    def __init__(self,
                 t: Type[T],
                 value: Union[T, None] = None,
                 *,
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[T, None] = None,
                 json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False,) -> None:
        self._t = t
        super().__init__(field, value, is_id, required, default,
                         json_field, indexable, filterable, exclude)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        if self._value is not None:
            for k, v in self._value.items():
                yield k, v

    def to_dict(self) -> TDict[str, Any]:
        if self._value is None:
            return {}
        return self._value.to_dict()

    def _ggt(self) -> Any:
        return lambda **kwargs: NonNull(self._t.to_graphql(), **kwargs)

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, JSON,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )
