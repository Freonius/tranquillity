from configparser import ConfigParser
from posixpath import abspath, isfile, exists
from typing import Any, Dict
from .__interface import ISettings


class Ini(ISettings):
    def __init__(self, ini_file: str) -> None:
        super().__init__()
        if not isinstance(ini_file, str):
            raise TypeError
        ini_file = abspath(ini_file)
        if not exists(ini_file) or not isfile(ini_file):
            raise Exception(f'The file {ini_file} does not exist')
        _conf: ConfigParser = ConfigParser()
        _conf.read(ini_file)
        del ini_file
        _d: Dict[str, Any] = {s: dict(_conf.items(s))
                              for s in _conf.sections()}
        del _conf
        self._config(_d)

    def _update(self, key: str, val: str) -> None:
        pass  # TODO: Update
