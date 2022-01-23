from abc import ABC
from typing import Any, Callable, Dict, List, Tuple, Union, Iterator
from inspect import getmembers
from json import loads, dumps
from copy import deepcopy
from .types._dtype import DType
from ..utils._classproperty import classproperty
from ..exceptions import ValidationError


class DataObject(ABC):
    __table__: str = NotImplemented
    __schema__: Union[str, None] = None
    __db__: Union[str, None] = None
    __data__: Dict[str, DType]

    def __init__(self, **data) -> None:
        self.__data__ = {}
        for dkey, dtype in self.get_fields_tuple():
            self.__data__[dkey] = deepcopy(dtype)
        for key, val in data.items():
            self[key] = val
        self.validate()

    @classproperty
    def table(cls) -> str:
        if cls.__schema__ is None:
            return cls.__table__
        return cls.__schema__ + '.' + cls.__table__

    @classmethod
    def filter(cls, objects: List['DataObject'], filter_fun: Callable[['DataObject'], bool]) -> List['DataObject']:

        out: List['DataObject'] = []
        for obj in objects:
            if isinstance(obj, cls) and filter_fun(obj):
                out.append(obj)
        return out

    def validate(self) -> None:
        pass    # TODO

    @property
    def is_valid(self) -> bool:
        try:
            self.validate()
            return True
        except ValidationError:
            return False

    def to_json(self) -> str:
        # TODO: Use json_field
        return dumps(dict(self))

    @classmethod
    def from_json(cls, body: str) -> 'DataObject':
        return cls(**loads(body))

    @classmethod
    def get_fields(cls) -> Iterator[DType]:
        for _fld_name, _fld_val in getmembers(cls):
            if isinstance(_fld_val, DType):
                if not isinstance(_fld_val.field, str):
                    _fld_val.field = _fld_name
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

    def keys(self) -> Iterator[str]:
        for fld, _ in self:
            yield fld

    def items(self) -> Iterator[Tuple[str, Any]]:
        for fld, val in self:
            yield fld, val

    def to_dict(self) -> Dict[str, Any]:
        return dict(self)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for _, fld in self.__data__.items():
            yield fld.field, fld.value

    def __repr__(self) -> str:
        _id: str = ' '.join(list([x.field + '=' + str(x.value)
                            for x in self.get_fields() if x.is_id]))
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
