from abc import ABC, abstractproperty
from typing import Any, Tuple, Type, Union, Generic, TypeVar, get_args

T = TypeVar('T')


class DType(ABC, Generic[T]):
    _field: str = NotImplemented
    _required: bool = True
    _nullable: bool = True
    _is_id: bool = False
    _default: Union[T, None] = None
    _json_field: Union[str, None] = None
    _value: Union[T, None] = None
    _t: Type[T] = NotImplemented

    @property
    def field(self) -> str:
        return self._field

    @field.setter
    def field(self, val: str) -> None:
        self._field = val

    @property
    def json_field(self) -> str:
        if self._json_field is None:
            return self._field
        return self._json_field

    @property
    def value(self) -> Union[T, None]:
        if self._value is None and self._nullable is False:
            if self._default is not None:
                return self._default
            raise ValueError
        return self._value

    @value.setter
    def value(self, val: Union[T, None]) -> None:
        if val is None and self._nullable is False:
            raise ValueError
        if not isinstance(val, self._t) and val is not None:
            raise TypeError
        self._value = val

    def set(self, val: T) -> None:
        self.value = val

    @property
    def is_id(self) -> bool:
        return self._is_id

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            if self.value == __o.value:
                return True
            return False
        if not isinstance(__o, type(self.value)):
            return False
        if self.value == __o:
            return True
        return False

    def __ne__(self, __o: object) -> bool:
        if self == __o:
            return False
        return True

    def __str__(self) -> str:
        return str(self.value)

    def __get__(self, instance, _) -> Union[T, None, 'DType']:
        if instance is None:
            return self
        if hasattr(instance, '__getitem__'):
            try:
                out = instance[self._field]
                if isinstance(out, self._t) or out is None:
                    return out
            except Exception:
                pass
        return self.value

    def __set__(self, instance, value: T) -> None:
        if hasattr(instance, '__setitem__'):
            try:
                instance[self._field] = value
            except Exception:
                pass
        self.value = value

    def __init__(self,
                 field: Union[str, None] = None,
                 value: Union[T, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[T, None] = None,
                 nullable: bool = True,
                 json_field: Union[str, None] = None) -> None:
        if field is not None:
            self._field = field
        self._is_id = is_id
        self._value = value
        self._required = required
        self._default = default
        self._nullable = nullable
        self._json_field = json_field

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self._field}={self._value}>'
