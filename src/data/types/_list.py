from typing import Generic, TypeVar, Type, Iterable, Union, List as TList, Any
from ._dtype import DType
from ._nested import Nested, Dict
from .._dataobject import DataObject

_T = TypeVar('_T')
T = TypeVar('T')


class Array(list, Generic[_T]):
    _t: Type[_T]

    def __init__(self, t: Type[_T], el: Union[Iterable[_T], None] = None) -> None:
        self._t = t
        super().__init__()
        if el is not None:
            for e in el:
                if not isinstance(e, self._t):
                    raise TypeError('Here')
            self.extend(el)

    @property
    def get_generic(self) -> Type[_T]:
        return self._t

    def append(self, __object: _T) -> None:
        if not isinstance(__object, self._t):
            raise TypeError
        return super().append(__object)

    def extend(self, __iterable: Iterable[_T]) -> None:
        for e in __iterable:
            if not isinstance(e, self._t):
                raise TypeError
        return super().extend(__iterable)


class List(DType[Array[T]], Generic[T]):
    _is_list = True
    _sub_t: Type[T]

    def __init__(self, t: Type[T], field: Union[str, None] = None, value: Union[Array[T], None] = None, is_id: bool = False, required: bool = True, default: Union[Array[T], None] = None, nullable: bool = True, json_field: Union[str, None] = None) -> None:
        self._t = Array
        self._sub_t = t
        self.value = value
        super().__init__(field, value, is_id, required, default, nullable, json_field)

    def to_list(self) -> Union[TList, None]:
        if self._value is None:
            return None
        _out: TList[Any] = []
        for x in self._value:
            if isinstance(x, (DataObject, Nested, Dict)):
                _out.append(x.to_dict())
            elif isinstance(x, type(self)):
                _out.append(x.to_list())
            else:
                _out.append(x)
        return _out

    @property
    def value(self) -> Union[Array[T], None]:
        if self._value is None and self._nullable is False:
            if self._default is not None:
                return self._default
            raise ValueError
        return self._value

    @value.setter
    def value(self, val: Union[Array[T], None]) -> None:
        if val is None and self._nullable is False:
            raise ValueError
        if isinstance(val, list):
            val = Array(self._sub_t, val)
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
