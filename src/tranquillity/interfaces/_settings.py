from abc import ABC
from typing import Any, Dict, List, Union

class ISettings(ABC):
    _data: Dict[str, str] = {}
    _raise_on_missing: bool = True

    def __init__(self,
                 file: Union[str, None] = None,
                 filetype: Union[str, None] = None,
                 debug: bool = False,
                 data: Union[Dict[str, Any], None] = None,
                 defaults: Union[Dict[str, Any], None] = None,
                 required_fields: Union[List[str], None] = None,
                 raise_on_missing: bool = True,
                 path: Union[str, None] = None,
                 file_ext: Union[str, None] = None,
                 read_only: bool = False,
                 dump_if_not_exists: bool = True):
        pass

    def __getitem__(self, key: str) -> Union[str, None]:
        return self.get(key=key, default=None)

    def __setitem__(self, key: str, val: str) -> None:
        pass

    def get(self, key: str, default: Union[str, None] = None) -> Union[str, None]:
        key = key.lower()
        if key not in self._data.keys():
            if default is not None:
                if isinstance(default, str):
                    return default
                raise TypeError(f'default value must be of type str, got {type(default)}')
            # TODO: Check if there is a global default
            elif self._raise_on_missing:
                raise KeyError(f'key "{key}" not found')
            return None
        return self._data[key]

    def set(self, key: str, val: str) -> None:
        pass
