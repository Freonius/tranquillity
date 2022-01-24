from typing import Any
from graphene import Boolean, NonNull
from ._dtype import DType
from ._nsdtype import NSDType


class Bool(DType[bool]):
    _t = bool

    def _ggt(self) -> Any:
        return Boolean


class NSBool(NSDType[bool]):
    _t = bool

    def _ggt(self) -> Any:
        return lambda **kwargs: NonNull(Boolean, **kwargs)
