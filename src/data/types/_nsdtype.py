from typing import Generic, Type
from types import NotImplementedType
from graphene import Field
from sqlalchemy import Column
from ._dtype import DType, T, Union


class NSDType(DType[T], Generic[T]):
    _value: T = NotImplemented
    _nullable = False

    @property
    def value(self) -> T:
        if isinstance(self._value, NotImplementedType):
            raise ValueError
        val = self._value_getter()
        if val is None:
            raise ValueError
        return val

    @value.setter
    def value(self, val: T) -> None:
        if isinstance(val, NotImplementedType):
            raise ValueError
        if val is None and self._nullable is False:
            raise ValueError
        self._value_setter(val)

    def __get__(self, instance, _) -> Union[T, 'NSDType']:
        if instance is None:
            return self
        if hasattr(instance, '__getitem__'):
            try:
                out = instance[self._field]
                if isinstance(out, self._t):
                    return out
            except Exception:
                pass
        return self.value

    def __init__(self,
                 field: Union[str, None] = None,
                 value: Union[T, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[T, None] = None,
                 json_field: Union[str, None] = None) -> None:
        if field is not None:
            self._field = field
        self._is_id = is_id
        self._required = required
        self._default = default
        self._json_field = json_field
        if value is not None:
            self.value = value

    def _ggt(self) -> Type[Field]:
        raise NotImplementedError

    def get_sqlalchemy_column(self) -> Column:
        raise NotImplementedError
