# pylint: disable=duplicate-code
from configparser import ConfigParser
from typing import Any, Dict, Union
from .__interface import ISettings


class Ini(ISettings):
    _file_name: str

    def __init__(self, ini_file: Union[str, None] = None) -> None:
        super().__init__()
        # if not isinstance(ini_file, str):
        #     raise TypeError
        ini_file = self._get_file_name(ini_file, 'ini')
        # if not exists(ini_file) or not isfile(ini_file):
        #     raise Exception(f'The file {ini_file} does not exist')
        _conf: ConfigParser = ConfigParser()
        _conf.read(ini_file)
        self._file_name = ini_file
        del ini_file
        _d: Dict[str, Any] = {s: dict(_conf.items(s))
                              for s in _conf.sections()}
        del _conf
        self._config(_d)

    def _update(self, key: str, val: str) -> None:
        _conf: ConfigParser = ConfigParser()
        _conf.read_dict(self._raw_data)
        with open(self._file_name, encoding='utf-8', mode='w') as _fh:
            _conf.write(_fh, space_around_delimiters=True)
