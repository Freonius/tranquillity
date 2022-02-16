from typing import Generic, TypeVar, Type, Iterable, Union, List as TList, Any
from sqlalchemy.types import ARRAY
from sqlalchemy import Column
from graphene import List as GList
from typing_utils import issubtype
from ._dtype import DType
from ._nested import Nested, Dict
from ._array import Array
from .._dataobject import DataObject
# TODO: sqlalchemy

T = TypeVar('T')


class List(DType[Array[T]], Generic[T]):
    _is_list = True
    _sub_t: Type[T]

    def get_type(self) -> Type[T]:  # type: ignore
        return self._sub_t

    def __init__(self,
                 t: Type[T],
                 value: Union[Array[T], None] = None,
                 *,
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[Array[T], None] = None,
                 nullable: bool = True,
                 json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False,) -> None:
        self._t = Array
        self._sub_t = t
        self.value = value
        super().__init__(field, value, is_id, required, default,
                         nullable, json_field, indexable, filterable, exclude)

    def to_list(self) -> Union[TList, None]:
        if self._value is None:
            return None
        _out: TList[Any] = []
        for x in self._value:
            if isinstance(x, (DataObject, Nested, Dict)):
                _out.append(x.serialize())
            elif isinstance(x, type(self)):
                _out.append(x.to_list())
            else:
                _out.append(x)
        return _out

    def _value_getter(self) -> Union[Array[T], None]:
        if self._value is None and self._nullable is False:
            if self._default is not None:
                return self._default
            raise ValueError
        return self._value

    def _value_setter(self, val: Union[Array[T], None]) -> None:
        if val is None and self._nullable is False:
            raise ValueError
        if isinstance(val, list):
            _temp_val: TList[Any] = []
            if issubtype(self._sub_t, DataObject):
                for v in val:
                    if isinstance(v, DataObject):
                        _temp_val.append(v)
                    elif isinstance(v, dict):
                        _temp_val.append(self._sub_t(**v))
                    else:
                        raise TypeError
            else:
                _temp_val = val
            val = Array(self._sub_t, _temp_val)
            del _temp_val
        if not isinstance(val, self._t) and val is not None:
            raise TypeError
        if val is not None and val.get_generic is not self._sub_t:
            raise TypeError
        self._value = val

    def append(self, val: T) -> None:
        if self._value is None:
            self._value = Array(self._sub_t)
        self._value.append(val)

    def extend(self, vals: Iterable[T]) -> None:
        if self._value is None:
            self._value = Array(self._sub_t)
        self._value.extend(vals)

    def get_sqlalchemy_column(self) -> Column:
        return Column(
            self.field, ARRAY(self._sub_t),
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )

    def _ggt(self) -> Any:
        return lambda **kwargs: GList(self._sub_t, **kwargs)
