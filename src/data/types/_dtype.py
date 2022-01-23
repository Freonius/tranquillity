from abc import ABC, abstractproperty
from typing import Any, Union, Generic, TypeVar

T = TypeVar('T')


class DType(ABC, Generic[T]):
    _field: str = NotImplemented
    _required: bool = True
    _nullable: bool = True
    _is_id: bool = False
    _default: Union[T, None] = None
    _json_field: Union[str, None] = None
    _value: Union[T, None] = None

    @property
    def field(self) -> str:
        return self._field

    @property
    def value(self) -> Union[T, None]:
        if self._value is None and self._nullable is False:
            if self._default is not None:
                return self._default
            raise ValueError
        return self._value

    @value.setter
    def value(self, val: T) -> None:
        pass

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
        return self.value

    def __set__(self, _, value: T) -> None:
        self.value = value
