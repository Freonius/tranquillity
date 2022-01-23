from abc import ABC
from typing import Any, Callable, Dict, List, Tuple, Union, Iterator
from inspect import getmembers
from json import loads, dumps
from .types._dtype import DType
from ..utils._classproperty import classproperty
from ..exceptions import ValidationError


class DataObject(ABC):
    __table__: str = NotImplemented
    __schema__: Union[str, None] = None
    __db__: Union[str, None] = None

    def __init__(self, **data) -> None:
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
        return dumps(dict(self))

    @classmethod
    def from_json(cls, body: str) -> 'DataObject':
        return cls(**loads(body))

    @classmethod
    def get_fields(cls) -> Iterator[DType]:
        for _, _fld_val in getmembers(cls):
            if isinstance(_fld_val, DType):
                yield _fld_val

    def __getitem__(self, key: str) -> Any:
        for fld in self.get_fields():
            if fld.field == key:
                return fld.value
        raise KeyError(f'Key {key} not found')

    def __setitem__(self, key: str, val: Any) -> None:
        for fld in self.get_fields():
            if fld.field == key:
                fld.value = val
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
        for fld in self.get_fields():
            yield fld.field, fld.value

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {" ".join(list([x.field + "=" + str(x.value) for x in self.get_fields() if x.is_id]))}>'

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
