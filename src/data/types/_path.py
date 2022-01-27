from typing import Union, Callable
from pathlib import Path as PPath
from os.path import expanduser, isdir, sep, isfile
from re import Pattern
from ._text import Text, NSText
from ...exceptions import ValidationError


def _convert(value: Union[str, None], absolute: bool) -> Union[str, None]:
    if value is None:
        return None
    if absolute:
        _tmp_val: PPath
        if value.startswith('~'):
            _tmp_val = PPath(expanduser(value)).absolute()
        elif value == 'home':
            _tmp_val = PPath(expanduser('~')).absolute()
        else:
            _tmp_val = PPath(value).absolute()
        value = str(_tmp_val)
    if isdir(value) and not value.endswith(sep):
        value += sep
    return value


def _validate(
        val: Union[str, None],
        check_dir: bool,
        check_file: bool,
        create: bool,
        mode: Union[int, None]) -> None:
    if val is None:
        return
    if mode is not None and (p := PPath(val)).exists():
        p.chmod(mode)
    if check_dir is True:
        if not isdir(val):
            if create is True:
                if mode is not None:
                    PPath(val).mkdir(mode=mode, parents=True)
                else:
                    PPath(val).mkdir(parents=True)
                return
            raise ValidationError
    if check_file is True:
        if not isfile(val):
            if create is True:
                if mode is not None:
                    PPath(val).touch(mode=mode)
                else:
                    PPath(val).touch()
                return
            raise ValidationError


class Path(Text):
    _absolute: bool = True
    _check_is_file: bool = False
    _check_is_dir: bool = False
    _create: bool = False
    _mode: Union[int, None] = None

    def _more_validation(self) -> None:
        super()._more_validation()
        _validate(self._value, self._check_is_dir,
                  self._check_is_file, self._create, self._mode)

    def _value_setter(self, val: Union[str, None]) -> None:
        super()._value_setter(val)
        self._value = _convert(self._value, self._absolute)

    def __init__(self,
                 value: Union[str, None] = None,
                 field: Union[str, None] = None,
                 primary_key: bool = False,
                 required: bool = True,
                 default: Union[str, None] = None,
                 absolute: bool = True,
                 check_is_file: bool = False,
                 check_is_dir: bool = False,
                 create: bool = False,
                 mode: Union[int, None] = None,
                 nullable: bool = True,
                 json_field: Union[str, None] = None,
                 not_empty: bool = False,
                 pattern: Union[Pattern[str], None, str] = None,
                 transform: Union[Callable[[str], str], None] = None,
                 min_length: Union[int, None] = None,
                 max_length: Union[int, None] = None,
                 auto_strip: bool = True,
                 uppercase: bool = False, lowercase: bool = False) -> None:
        self._absolute = absolute
        self._check_is_dir = check_is_dir
        self._check_is_file = check_is_file
        self._create = create
        self._mode = mode
        super().__init__(value, field, primary_key, required, default, nullable, json_field,
                         not_empty, pattern, transform, min_length, max_length,
                         auto_strip, uppercase, lowercase)


class NSPath(NSText):
    _absolute: bool = True
    _check_is_file: bool = False
    _check_is_dir: bool = False
    _create: bool = False
    _mode: Union[int, None] = None

    def _more_validation(self) -> None:
        super()._more_validation()
        _validate(self._value, self._check_is_dir,
                  self._check_is_file, self._create, self._mode)

    def _value_setter(self, val: Union[str, None]) -> None:
        super()._value_setter(val)
        if (val := _convert(self._value, self._absolute)) is not None:
            self._value = val

    def __init__(self,
                 value: Union[str, None] = None,
                 field: Union[str, None] = None,
                 primary_key: bool = False,
                 required: bool = True,
                 default: Union[str, None] = None,
                 absolute: bool = True,
                 check_is_file: bool = False,
                 check_is_dir: bool = False,
                 create: bool = False,
                 mode: Union[int, None] = None,
                 json_field: Union[str, None] = None,
                 not_empty: bool = False,
                 pattern: Union[Pattern[str], None, str] = None,
                 transform: Union[Callable[[str], str], None] = None,
                 min_length: Union[int, None] = None,
                 max_length: Union[int, None] = None,
                 auto_strip: bool = True,
                 uppercase: bool = False, lowercase: bool = False) -> None:
        self._absolute = absolute
        self._check_is_dir = check_is_dir
        self._check_is_file = check_is_file
        self._create = create
        self._mode = mode
        super().__init__(value, field, primary_key, required, default, json_field,
                         not_empty, pattern, transform, min_length, max_length,
                         auto_strip, uppercase, lowercase)
