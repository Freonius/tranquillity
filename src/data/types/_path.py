from typing import Union
from pathlib import Path as PPath
from os.path import expanduser, isdir, sep
from ._text import Text, NSText


class Path(Text):
    _absolute: bool

    def _more_validation(self) -> None:
        return super()._more_validation()

    def _value_setter(self, val: Union[str, None]) -> None:
        super()._value_setter(val)
        if self._value is None:
            return

        if self._absolute:
            _tmp_val: PPath
            if self._value.startswith('~'):
                _tmp_val = PPath(expanduser(self._value)).absolute()
            elif self._value == 'home':
                _tmp_val = PPath(expanduser('~')).absolute()
            else:
                _tmp_val = PPath(self._value).absolute()
            self._value = str(_tmp_val)
        if isdir(self._value) and not self._value.endswith(sep):
            self._value += sep
