from os.path import abspath, isfile, exists
from typing import Dict, Any
from configparser import RawConfigParser
from .__interface import ISettings


class Properties(ISettings):
    def __init__(self, prop_file: str) -> None:
        super().__init__()
        if not isinstance(prop_file, str):
            raise TypeError
        prop_file = abspath(prop_file)
        if not exists(prop_file) or not isfile(prop_file):
            raise Exception(f'The file {prop_file} does not exist')
        _conf: RawConfigParser = RawConfigParser()
        _conf.read(prop_file)
        del prop_file
        _d: Dict[str, Any] = {s: dict(_conf.items(s))
                              for s in _conf.sections()}
        del _conf
        self._config(_d)

    def _update(self, key: str, val: str) -> None:
        pass  # TODO: Update # pragma: no cover
