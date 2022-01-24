from abc import ABC, abstractclassmethod, abstractmethod
from types import NotImplementedType
from typing import Any, Dict, Tuple, Type, Union, Generic, TypeVar, List
from graphene import Field
from ...exceptions import ValidationError

T = TypeVar('T')


class DType(ABC, Generic[T]):
    _field: str = NotImplemented
    _required: bool = True
    _nullable: bool = True
    _is_id: bool = False
    _default: Union[T, None] = None
    _json_field: Union[str, None] = None
    _value: Union[T, None] = None
    _unique: bool = False
    _is_dict: bool = False
    _is_list: bool = False
    _t: Type[T] = NotImplemented

    def get_type(self) -> Type[T]:
        return self._t

    @property
    def is_dict(self) -> bool:
        return self._is_dict

    @property
    def is_list(self) -> bool:
        return self._is_list

    @property
    def field(self) -> str:
        return self._field

    @field.setter
    def field(self, val: str) -> None:
        self._field = val

    @property
    def is_nullable(self) -> bool:
        return self._nullable

    @property
    def json_field(self) -> str:
        if self._json_field is None:
            return self._field
        return self._json_field

    @property
    def value(self) -> Union[T, None]:
        if isinstance(self._value, NotImplementedType):
            self._value = None
        if self._value is None and self._nullable is False:
            if self._default is not None:
                return self._default
            raise ValueError
        return self._value

    @value.setter
    def value(self, val: Union[T, None]) -> None:
        if isinstance(val, NotImplementedType):
            val = None
        if val is None and self._nullable is False:
            raise ValueError
        if val is not None:
            val = self._transform_fun(val)
        if not isinstance(val, self._t) and val is not None:
            raise TypeError
        self._value = val

    def set(self, val: T) -> None:
        self.value = val

    @property
    def is_valid(self) -> bool:
        try:
            self.validate()
            return True
        except ValidationError:
            return False

    def validate(self) -> None:
        if isinstance(self._value, NotImplementedType):
            raise ValidationError('value is not implemented')
        self._more_validation()
        if self._value is None and self._nullable is False:
            if self._default is None and not isinstance(self._default, self._t):
                raise ValidationError('value cannot be null')

    @property
    def is_id(self) -> bool:
        return self._is_id

    def is_primary_key(self) -> bool:
        return self._is_id

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            if self.value == __o.value:
                return True
            return False
        if not isinstance(__o, self._t):
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

    def __delete__(self, _) -> None:
        self._value = None

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

    def _more_validation(self) -> None:
        pass

    def _transform_fun(self, val: T) -> T:
        return val

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self._field}={self._value}>'

    def to_dict(self) -> Union[Dict[str, Any], None]:
        return None

    def to_list(self) -> Union[List[Any], None]:
        return None

    def iter_value(self) -> Union[T, None, List[Any], Dict[str, Any]]:
        if self._is_dict is True:
            return self.to_dict()
        if self._is_list is True:
            return self.to_list()
        return self.value

    def serialize(self) -> Union[T, None, List[Any], Dict[str, Any]]:
        return self.iter_value()

    @abstractmethod
    def _ggt(self) -> Type[Field]:
        pass

    def get_graphql_type(self) -> Field:
        def _resolver(root, info, *args, **kwargs):
            _fld = root.__data__[info.field_name]
            return _fld

        _out = self._ggt()(name=self.json_field,
                           default_value=self._default, resolver=_resolver)

        return _out
