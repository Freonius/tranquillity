from typing import Union, Tuple, Iterable, Any
from graphene import Float as GqlFloat, NonNull
from ._dtype import DType
from ._nsdtype import NSDType
from ...exceptions import ValidationError


def _val(_value: Union[float, None], _gt_zero: bool, _ge_zero: bool, _between: Union[Tuple[float, float], None], _in: Union[None, Iterable[float]]) -> None:
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


class Float(DType[float]):
    _t = float
    _gt_zero: bool = False
    _ge_zero: bool = False
    _between: Union[Tuple[float, float], None] = None
    _in: Union[None, Iterable[float]] = None

    def __init__(self,
                 value: Union[float, None] = None,
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[float, None] = None,
                 nullable: bool = True,
                 json_field: Union[str, None] = None,
                 ) -> None:
        super().__init__(field, value, is_id, required, default, nullable, json_field)

    def _more_validation(self) -> None:
        _val(self._value, self._gt_zero, self._ge_zero, self._between, self._in)

    def _ggt(self) -> Any:
        return GqlFloat


class NSFloat(NSDType[float]):
    _t = float
    _gt_zero: bool = False
    _ge_zero: bool = False
    _between: Union[Tuple[float, float], None] = None
    _in: Union[None, Iterable[float]] = None

    def __init__(self,
                 value: Union[float, None] = None,
                 field: Union[str, None] = None,
                 is_id: bool = False,
                 required: bool = True,
                 default: Union[float, None] = None,
                 json_field: Union[str, None] = None,
                 ) -> None:
        super().__init__(field, value, is_id, required, default, json_field)

    def _more_validation(self) -> None:
        _val(self._value, self._gt_zero, self._ge_zero, self._between, self._in)

    def _ggt(self) -> Any:
        return lambda **kwargs: NonNull(GqlFloat, **kwargs)
