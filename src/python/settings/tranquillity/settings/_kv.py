from typing import Any, Dict, Union
from .__interface import ISettings


class KVSetting(ISettings):
    def __init__(self, data: Union[Dict[str, Any], None] = None) -> None:
        super().__init__()
        if data is None:
            data = {}
        self._config(data)

    def _update(self, key: str, val: str) -> None:
        self._data[key] = val
