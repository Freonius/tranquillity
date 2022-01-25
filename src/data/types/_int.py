from typing import Iterable, Tuple, Union, Any
from graphene import Int as GqlInt, NonNull
from ._dtype import DType
from ._nsdtype import NSDType
from ...exceptions import ValidationError


def _val(_value: Union[int, None], _gt_zero: bool, _ge_zero: bool, _between: Union[Tuple[int, int], None], _in: Union[None, Iterable[int]]) -> None:
    if _value is None:
        return
    if _gt_zero and _value < 0:
        raise ValidationError
    if _ge_zero and _value <= 0:
        raise ValidationError
    if _between is not None:
        if _value < min(_between) or _value > max(_between):
            raise ValidationError
    if _in is not None and _value not in _in:
        raise ValidationError


class Int(DType[int]):
    _t = int
    _gt_zero: bool = False
    _ge_zero: bool = False
    _between: Union[Tuple[int, int], None] = None
    _in: Union[None, Iterable[int]] = None

    def _more_validation(self) -> None:
        _val(self._value, self._gt_zero, self._ge_zero, self._between, self._in)

    def _ggt(self) -> Any:
        return GqlInt


class NSInt(NSDType[int]):
    _t = int
    _gt_zero: bool = False
    _ge_zero: bool = False
    _between: Union[Tuple[int, int], None] = None
    _in: Union[None, Iterable[int]] = None

    def _more_validation(self) -> None:
        _val(self._value, self._gt_zero, self._ge_zero, self._between, self._in)

    def _ggt(self) -> Any:
        return lambda **kwargs: NonNull(GqlInt, **kwargs)
