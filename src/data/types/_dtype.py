from abc import ABC, abstractmethod
from types import NotImplementedType
from typing import Any, Callable, Dict, Type, Union, Generic, TypeVar, List
from graphene import Field
from pandas import isna
from sqlalchemy import Column
from ...exceptions import ValidationError
from ...connections import IConnection
from ...query._dataclasses import WhereCondition
from ...query._values import QWhereV, QWhereVR
from ...query._enums import QueryJoin, QueryComparison, QueryType
from ...query._utils import type_to_querytype

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
    _is_filterable: bool = True
    _is_indexable: bool = True
    _exclude_from_json: bool = False

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
    def is_indexable(self) -> bool:
        return self._is_indexable

    @property
    def is_filterable(self) -> bool:
        return self._is_filterable

    @property
    def exclude_from_json(self) -> bool:
        return self._exclude_from_json

    @property
    def json_field(self) -> str:
        if self._json_field is None:
            return self._field
        return self._json_field

    @property
    def value(self) -> Union[T, None]:
        return self._value_getter()

    @value.setter
    def value(self, val: Union[T, None]) -> None:
        self._value_setter(val)

    def _value_getter(self) -> Union[T, None]:
        if isinstance(self._value, NotImplementedType):
            self._value = None
        if self._value is None and self._nullable is False:
            if self._default is not None:
                return self._default
            raise ValueError
        if self._value is None and self._default is not None:
            return self._default
        return self._value

    def _value_setter(self, val: Union[T, None]) -> None:
        if isinstance(val, NotImplementedType):
            val = None
        if isna(val) is True:
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

    @property
    def is_primary_key(self) -> bool:
        return self._is_id

    def __eq__(self, __o: object) -> Union[WhereCondition, bool]: # type: ignore
        if isinstance(__o, type(self)):
            if self.value == __o.value:
                return True
            return False
        _wc: WhereCondition = WhereCondition(
            join=QueryJoin.And,
            field=self.field,
            type=type_to_querytype(self._t, self.is_list),
            comparison=QueryComparison.Eq,
            value=QWhereV(__o)
        )
        return _wc

    def __ne__(self, __o: object) -> Union[WhereCondition, bool]: # type: ignore
        if isinstance(__o, type(self)):
            if self.value != __o.value:
                return True
            return False
        _wc: WhereCondition = WhereCondition(
            join=QueryJoin.And,
            field=self.field,
            type=type_to_querytype(self._t, self.is_list),
            comparison=QueryComparison.Ne,
            value=QWhereV(__o)
        )
        return _wc

    def __gt__(self, __o: object) -> Union[WhereCondition, bool]: # type: ignore
        if isinstance(__o, type(self)):
            return False
        _wc: WhereCondition = WhereCondition(
            join=QueryJoin.And,
            field=self.field,
            type=type_to_querytype(self._t, self.is_list),
            comparison=QueryComparison.Gt,
            value=QWhereV(__o)
        )
        return _wc

    def __ge__(self, __o: object) -> Union[WhereCondition, bool]: # type: ignore
        if isinstance(__o, type(self)):
            return False
        _wc: WhereCondition = WhereCondition(
            join=QueryJoin.And,
            field=self.field,
            type=type_to_querytype(self._t, self.is_list),
            comparison=QueryComparison.Gte,
            value=QWhereV(__o)
        )
        return _wc

    def __lt__(self, __o: object) -> Union[WhereCondition, bool]: # type: ignore
        if isinstance(__o, type(self)):
            return False
        _wc: WhereCondition = WhereCondition(
            join=QueryJoin.And,
            field=self.field,
            type=type_to_querytype(self._t, self.is_list),
            comparison=QueryComparison.Lt,
            value=QWhereV(__o)
        )
        return _wc

    def __le__(self, __o: object) -> Union[WhereCondition, bool]: # type: ignore
        if isinstance(__o, type(self)):
            return False
        _wc: WhereCondition = WhereCondition(
            join=QueryJoin.And,
            field=self.field,
            type=type_to_querytype(self._t, self.is_list),
            comparison=QueryComparison.Lte,
            value=QWhereV(__o)
        )
        return _wc

    def __contains__(self, __o: object) -> Union[WhereCondition, bool]: # type: ignore
        if isinstance(__o, type(self)):
            return False
        if not isinstance(__o, (list, tuple)):
            raise TypeError
        if len(__o) != 2:
            raise TypeError
        _wc: WhereCondition = WhereCondition(
            join=QueryJoin.And,
            field=self.field,
            type=type_to_querytype(self._t, self.is_list),
            comparison=QueryComparison.Between,
            value=QWhereVR(__o[0], __o[1])
        )
        return _wc

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
                 json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False,) -> None:
        if field is not None:
            self._field = field
        self._is_id = is_id
        self._value = value
        self._required = required
        self._default = default
        self._nullable = nullable
        self._json_field = json_field
        self._exclude_from_json = exclude
        self._is_filterable = filterable
        self._is_indexable = indexable

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

    def iter_value(self) -> Union[T, str, None, List[Any], Dict[str, Any]]:
        if self._is_dict is True:
            return self.to_dict()
        if self._is_list is True:
            return self.to_list()
        return self.value

    def serialize(self) -> Union[T, str, None, List[Any], Dict[str, Any]]:
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

    @abstractmethod
    def get_sqlalchemy_column(self) -> Column:
        pass
