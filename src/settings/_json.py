# pylint: disable=duplicate-code
from typing import Any, Dict, Union
from json import loads, dumps
from .__interface import ISettings


class Json(ISettings):
    _file_name: str

    def __init__(self, json_file: Union[str, None] = None,
                 defaults: Union[Dict[str, Any], None] = None,
                 raise_on_missing: bool = True,
                 read_only: bool = False) -> None:
        super().__init__()
        json_file = self._get_file_name(json_file, 'json')
        _d: Dict[str, Any] = {}
        with open(json_file, encoding='utf-8') as _fh:
            _d = loads(_fh.read())
        self._file_name = json_file
        del json_file
        self._config(_d, defaults=defaults,
                     raise_on_missing=raise_on_missing,
                     read_only=read_only)

    def _update(self, key: str, val: str) -> None:
        with open(self._file_name, mode='w', encoding='utf-8') as _fh:
            _fh.write(dumps(self._raw_data))
