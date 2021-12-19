# pylint: disable=duplicate-code
from typing import Any, Dict, Union
from yaml import load
from yaml.loader import SafeLoader
from .__interface import ISettings


class Yaml(ISettings):
    def __init__(self, yaml_file: Union[str, None] = None,
                 defaults: Union[Dict[str, Any], None] = None,
                 raise_on_missing: bool = True,
                 read_only: bool = False) -> None:
        super().__init__()
        yaml_file = self._get_file_name(yaml_file, 'yml0')
        _d: Dict[str, Any] = {}
        with open(yaml_file, encoding='utf-8') as _fh:
            _d = load(_fh.read(), SafeLoader)
        del yaml_file
        self._config(_d, defaults=defaults,
                     raise_on_missing=raise_on_missing,
                     read_only=read_only)

    def _update(self, key: str, val: str) -> None:
        pass  # TODO: Update
