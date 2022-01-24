from typing import Generic
from ._dtype import DType, T, Union


class NSDType(DType[T], Generic[T]):
    _value: T = NotImplemented
    _nullable = False

    @property
    def value(self) -> T:
        if self._value is None and self._nullable is False:
            if self._default is not None:
                return self._default
            raise ValueError
        if not isinstance(self._value, self._t):
            raise TypeError
        return self._value

    @value.setter
    def value(self, val: T) -> None:
        if val is None and self._nullable is False:
            raise ValueError
        if not isinstance(val, self._t) and val is not None:
            raise TypeError
        val = self._transform_fun(val)
        self._value = val

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
        if value is not None:
            self.value = value
        self._required = required
        self._default = default
        self._json_field = json_field
