from typing import Any, Union, Callable, List
from re import Pattern, match, Match, compile
from graphene import NonNull, String as GqlString
from sqlalchemy import Column, String as SqlString, Constraint, CheckConstraint
from ._dtype import DType
from ._nsdtype import NSDType
from ...exceptions import ValidationError


def _more_validation(
        val: Union[str, None],
        ne: bool,
        m: Union[Pattern, None],
        min_len: Union[int, None],
        max_len: Union[int, None]) -> None:
    if val is None:
        return
    if ne is True and len(val.strip()) == 0:
        raise ValidationError('String cannot be empty')
    if min_len is not None and len(val.strip()) < min_len:
        raise ValidationError(
            f'String must be at least {min_len} characters long')
    if max_len is not None and len(val) > max_len:
        raise ValidationError(
            f'String cannot be longer than {max_len} characters')
    if m is not None and isinstance(m, Pattern):
        _match: Union[Match, None] = match(m, val)
        if _match is None:
            raise ValidationError(f'String does not conform to pattern {m}')


def _transform_val(val: str,
                   tr: Union[Callable[[str], str], None],
                   autostrip: bool, lower: bool, upper: bool) -> str:
    if autostrip is True:
        val = val.strip()
    if lower is True:
        val = val.lower()
    if upper is True:
        val = val.upper()
    if tr is None:
        return val
    return tr(val)


class Text(DType[str]):
    _t = str
    _not_empty: bool = False
    _pattern: Union[Pattern[str], None] = None
    _transform: Union[Callable[[str], str], None] = None
    _min_len: Union[int, None] = None
    _max_len: Union[int, None] = None
    _autostrip: bool = True
    _upper: bool = False
    _lower: bool = False

    def __init__(self,
                 value: Union[str, None] = None,
                 field: Union[str, None] = None,
                 primary_key: bool = False,
                 required: bool = True,
                 default: Union[str, None] = None,
                 nullable: bool = True,
                 json_field: Union[str, None] = None,
                 not_empty: bool = False,
                 pattern: Union[Pattern[str], None, str] = None,
                 transform: Union[Callable[[str], str], None] = None,
                 min_length: Union[int, None] = None,
                 max_length: Union[int, None] = None,
                 auto_strip: bool = True,
                 uppercase: bool = False,
                 lowercase: bool = False,
                 ) -> None:
        self._not_empty = not_empty
        if isinstance(pattern, str):
            pattern = compile(pattern)
        self._pattern = pattern
        self._transform = transform
        self._min_len = min_length
        self._max_len = max_length
        if uppercase is True and lowercase is True:
            raise ValueError(
                'uppercase and lowercase cannot be both true, and yet they are')
        self._autostrip = auto_strip
        self._upper = uppercase
        self._lower = lowercase
        super().__init__(field, value, primary_key, required, default, nullable, json_field)

    def _more_validation(self) -> None:
        _more_validation(self._value, self._not_empty,
                         self._pattern, self._min_len, self._max_len)

    def _transform_fun(self, val: str) -> str:
        return _transform_val(val, self._transform, self._autostrip,
                              self._lower, self._upper)

    def _ggt(self) -> Any:
        return GqlString

    def get_sqlalchemy_column(self) -> Column:
        constrainst: List[Constraint] = []
        if self._min_len is not None:
            constrainst.append(CheckConstraint(
                f'LENGTH({self.field}) >= {self._min_len}',))
        if self._max_len is True:
            constrainst.append(CheckConstraint(
                f'LENGTH({self.field}) <= {self._max_len}',))
        return Column(
            self.field, SqlString,
            *constrainst,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )


class NSText(NSDType[str]):
    _t = str
    _not_empty: bool = False
    _pattern: Union[Pattern, None] = None
    _transform: Union[Callable[[str], str], None] = None
    _min_len: Union[int, None] = None
    _max_len: Union[int, None] = None
    _autostrip: bool = True
    _upper: bool = False
    _lower: bool = False

    def __init__(self,
                 value: Union[str, None] = None,
                 field: Union[str, None] = None,
                 primary_key: bool = False,
                 required: bool = True,
                 default: Union[str, None] = None,
                 json_field: Union[str, None] = None,
                 not_empty: bool = False,
                 pattern: Union[Pattern[str], None, str] = None,
                 transform: Union[Callable[[str], str], None] = None,
                 min_length: Union[int, None] = None,
                 max_length: Union[int, None] = None,
                 auto_strip: bool = True,
                 uppercase: bool = False,
                 lowercase: bool = False,
                 ) -> None:
        self._not_empty = not_empty
        if isinstance(pattern, str):
            pattern = compile(pattern)
        self._pattern = pattern
        self._transform = transform
        self._min_len = min_length
        self._max_len = max_length
        if uppercase is True and lowercase is True:
            raise ValueError(
                'uppercase and lowercase cannot be both true, and yet they are')
        self._autostrip = auto_strip
        self._upper = uppercase
        self._lower = lowercase
        super().__init__(field, value, primary_key, required, default, json_field)

    def _more_validation(self) -> None:
        _more_validation(self._value, self._not_empty,
                         self._pattern, self._min_len, self._max_len)

    def _transform_fun(self, val: str) -> str:
        return _transform_val(val, self._transform, self._autostrip,
                              self._lower, self._upper)

    def _ggt(self) -> Any:
        return lambda **kwargs: NonNull(GqlString, **kwargs)

    def get_sqlalchemy_column(self) -> Column:
        constrainst: List[Constraint] = []
        if self._min_len is not None:
            constrainst.append(CheckConstraint(
                f'LENGTH({self.field}) >= {self._min_len}',))
        if self._max_len is True:
            constrainst.append(CheckConstraint(
                f'LENGTH({self.field}) <= {self._max_len}',))
        return Column(
            self.field, SqlString,
            *constrainst,
            default=self._default,
            nullable=self._nullable,
            primary_key=self.is_primary_key,
        )


class String(Text):
    pass


class NSString(NSText):
    pass
