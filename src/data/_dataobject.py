from abc import ABC
from typing import Any, Callable, Dict, List, Tuple, Union, Iterator, Iterable, TypeVar, Type
from inspect import getmembers
from json import loads, dumps
from copy import deepcopy
from attr import attrs
from rule_engine import type_resolver_from_dict, Context, DataType, Rule
from graphene import ObjectType, String, Schema, Field
from .types._dtype import DType
from ..utils._classproperty import classproperty
from ..exceptions import ValidationError

T = TypeVar('T', bound='DataObject')


class DataObject(ABC):
    __table__: str = NotImplemented
    __schema__: Union[str, None] = None
    __db__: Union[str, None] = None
    __data__: Dict[str, DType]

    def __init__(self: T, **data) -> None:
        self.__data__ = {}
        for dkey, dtype in self.get_fields_tuple():
            self.__data__[dkey] = deepcopy(dtype)
        for key, val in data.items():
            self[key] = val
        # self.validate()

    @classproperty
    def table(cls) -> str:
        if cls.__schema__ is None:
            return cls.__table__
        return cls.__schema__ + '.' + cls.__table__

    @classmethod
    def graphql(cls) -> Type[ObjectType]:
        flds = cls.get_fields_tuple()
        return type('GQL' + cls.__class__.__name__, (ObjectType,), {
            x[0]: x[1].get_graphql_type() for x in flds
        })

    def get_graphql_type(self) -> ObjectType:
        attr = {
            x[0]: x[1].get_graphql_type() for x in self.__data__.items()
        }

        def _look(s, k):
            try:
                return s.__data__[k].value
            except:
                for _, f in s.__data__.items():
                    if f.fiels == k:
                        return f.value
        attr['__data__'] = deepcopy(self.__data__)
        attr['__getitem__'] = lambda s, k: _look(s, k)
        for x, _ in self.__data__.items():
            attr['resolve_' + x] = lambda s, *a, **k: s[x]
        attr['resolve_filter'] = lambda s, *a, **k: 'I am a filter'
        return type('GQL' + self.__class__.__name__, (ObjectType,), attr)

    def serialize(self) -> Dict[str, Any]:
        return self.to_dict()

    @classmethod
    def get_rule_engine_context(cls: Type[T]) -> Context:
        _ctx: Dict[str, Any] = {}
        for fld in cls.get_fields():
            _t_ctx: Union[None, Any] = None
            try:
                _t_ctx = DataType.from_type(fld.get_type())
            except ValueError:
                if fld.is_dict:
                    _t_ctx = DataType.MAPPING(
                        DataType.STRING, DataType.UNDEFINED, fld.is_nullable)
                else:
                    _t_ctx = DataType.UNDEFINED
            if fld.is_list:
                _t_ctx = DataType.ARRAY(_t_ctx, fld.is_nullable)
            if _t_ctx is None:
                _t_ctx = DataType.UNDEFINED
            _ctx[fld.field] = _t_ctx
        return Context(type_resolver=type_resolver_from_dict(_ctx))

    @classmethod
    def filter_re_rule(cls, objects: Iterable[T], rule: str) -> List[T]:
        out: List[T] = []
        re_rule: Rule = Rule(rule, context=cls.get_rule_engine_context())
        for o in objects:
            if re_rule.matches(o.to_dict()):
                out.append(o)
        return out

    @classmethod
    def filter(cls: Type[T], objects: Iterable[T], filter_fun: Callable[[T], bool]) -> List[T]:

        out: List[T] = []
        for obj in objects:
            if isinstance(obj, cls) and filter_fun(obj):
                out.append(obj)
        return out

    def validate(self) -> None:
        for _, fld in self.__data__.items():
            fld.validate()

    @property
    def is_valid(self) -> bool:
        try:
            self.validate()
            return True
        except ValidationError:
            return False

    def to_json(self) -> str:
        out: Dict[str, Any] = {}
        for _, fld in self.__data__.items():
            out[fld.json_field] = fld.serialize()
        return dumps(out, indent=None)

    @classmethod
    def from_json(cls, body: str) -> 'DataObject':
        return cls(**loads(body))

    @classmethod
    def get_fields(cls) -> Iterator[DType]:
        for _fld_name, _fld_val in getmembers(cls):
            if isinstance(_fld_val, DType):
                if not isinstance(_fld_val.field, str):
                    _fld_val.field = _fld_name
                # if isinstance(_fld_val, Enum):
                #     print(_fld_name)
                #     _fld_val.field = _fld_name
                #     _fld_val.value = _fld_name
                yield _fld_val

    @classmethod
    def get_fields_tuple(cls) -> Iterator[Tuple[str, DType]]:
        for _fld_name, _fld_val in getmembers(cls):
            if isinstance(_fld_val, DType):
                if not isinstance(_fld_val.field, str):
                    _fld_val.field = _fld_name
                yield _fld_name, _fld_val

    def __getitem__(self, key: str) -> Any:
        for _fld_name, _fld_val in self.__data__.items():
            if key in (_fld_name, _fld_val.field, _fld_val.json_field):
                return _fld_val.value
        raise KeyError(f'Key {key} not found')

    def __setitem__(self, key: str, val: Any) -> None:
        for _fld_name, _fld_val in self.__data__.items():
            if key in (_fld_name, _fld_val.field, _fld_val.json_field):
                _fld_val.value = val
                return
        raise KeyError(f'Key {key} not found')

    def get(self, key: str) -> Any:
        return self[key]

    def set(self, key: str, val: str) -> None:
        self[key] = val

    def keys(self) -> Iterator[str]:
        for fld, _ in self:
            yield fld

    def items(self) -> Iterator[Tuple[str, Any]]:
        for fld, val in self:
            yield fld, val

    def to_dict(self) -> Dict[str, Any]:
        _out: Dict[str, Any] = {}
        for _k, _v in self:
            _out[_k] = _v
        return _out

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for _, fld in self.__data__.items():
            yield fld.field, deepcopy(fld.iter_value())

    def __repr__(self) -> str:
        _id: str = ' '.join(list([x[1].field + '=' + str(x[1])
                            for x in self.__data__.items() if x[1].is_id]))
        _id = _id.strip()
        _sp: str = ' ' if len(_id) > 0 else ''
        return f'<{self.__class__.__name__}{_sp}{_id}>'

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, type(self)):
            return False
        for a, _ in self:
            if self[a] != __o[a]:
                return False
        return True

    def __ne__(self, __o: object) -> bool:
        if self == __o:
            return False
        return True
