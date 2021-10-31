from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Tuple, Union
from ..exceptions import NotAllowedOperation, ConversionError

class ISettings(ABC):
    _data: Dict[str, str] = {}
    _raise_on_missing: bool = True
    _defaults: Union[Dict[str, Any], None] = None
    _debug: bool = False
    _read_only: bool = False

    def _config(self,
                 file: Union[str, None] = None,
                 settings_type: Union[str, None] = None,
                 debug: bool = False,
                 data: Union[Dict[str, Any], None] = None,
                 defaults: Union[Dict[str, Any], None] = None,
                 required_fields: Union[List[str], None] = None,
                 raise_on_missing: bool = True,
                 path: Union[str, None] = None,
                 file_ext: Union[str, None] = None,
                 read_only: bool = False,
                 dump_if_not_exists: bool = True,
                 **kwargs):
        if defaults is not None and isinstance(defaults, dict):
            pass
        elif defaults is not None:
            if __debug__:
                raise TypeError(f'defaults must be of type None or dict, got {type(defaults)}')
            else:
                raise TypeError('defaults must be of type None or dict')
        # read_only
        if isinstance(read_only, bool):
            self._read_only = read_only
        elif read_only is None:
            self._read_only = False
        elif isinstance(read_only, int):
            if read_only <= 0:
                self._read_only = False
            else:
                self._read_only = True
        elif isinstance(read_only, str):
            self._read_only = False if str(read_only).lower() in {'f', 'false', 'n', 'no'} else True
        else:
            if __debug__:
                raise TypeError(f'read_only must be of type bool, got {type(read_only)}')
            else:
                raise TypeError('read_only must be of type bool')

        if isinstance(debug, bool):
            self._debug = debug
        elif debug is None:
            self._debug = False
        else:
            self._debug = __debug__

    @abstractmethod
    def __load__(self) -> None:
        pass

    def __getitem__(self, key: str) -> Union[str, None]:
        return self.get(key=key, default=None)

    def __setitem__(self, key: str, val: str) -> None:
        self.set(key=key, val=val)

    def get(self, key: str, default: Union[str, None] = None) -> Union[str, None]:
        if not isinstance(key, str):
            raise TypeError(f'key must be of type str, got {type(key)}')
        key = key.lower()
        if key not in self._data.keys():
            if default is not None:
                if isinstance(default, str):
                    return default
                raise TypeError(f'default value must be of type str, got {type(default)}')
            elif self._defaults is not None:
                if key in self._defaults.keys():
                    return self._defaults[key]
                elif self._raise_on_missing:
                    raise KeyError(f'key "{key}" not found')
            elif self._raise_on_missing:
                raise KeyError(f'key "{key}" not found')
            return None
        return self._data[key]

    def set(self, key: str, val: str) -> None:
        if self._read_only:
            raise NotAllowedOperation(f'{type(self)} was marked as read only')
        if not isinstance(key, str):
            raise TypeError(f'key must be of type str, got {type(key)}')
        if not isinstance(val, str):
            raise TypeError(f'val must be of type str, got {type(val)}')
        key = key.lower()
        self._data[key] = val

    def get_int(self, key: str, default: Union[int, None] = None) -> Union[int, None]:
        if default is not None and not isinstance(default, int):
            raise TypeError('default must be of type int')
        tmp: Union[str, None] = self.get(key, str(default) if default is not None else None)
        if tmp is None:
            return None
        try:
            return int(tmp)
        except ValueError as ex:
            raise ConversionError(f'Could not convert "{tmp}" to int') from ex

    def get_float(self, key: str, default: Union[float, None] = None) -> Union[float, None]:
        if default is not None and not isinstance(default, float):
            raise TypeError('default must be of type float')
        tmp: Union[str, None] = self.get(key, str(default) if default is not None else None)
        if tmp is None:
            return None
        try:
            return float(tmp)
        except ValueError as ex:
            raise ConversionError(f'Could not convert "{tmp}" to float') from ex

    def get_bool(self, key: str, default: Union[bool, None] = None) -> bool:
        if default is not None and not isinstance(default, float):
            raise TypeError('default must be of type float')
        tmp: Union[str, None] = self.get(key, str(default) if default is not None else None)
        if tmp is None:
            return False
        tmp = tmp.lower().strip()
        if len(tmp) == 0:
            return False
        if tmp.isdigit():
            if int(tmp) >= 1:
                return True
            else:
                return False
        if tmp in {'true', 't', 'yes', 'y', 'ok'}:
            return True
        else:
            return False

    def __iter__(self) -> Iterable[Tuple[str, str]]:
        key: str
        val: str
        for key, val in self._data.items():
            yield key, val

    def keys(self) -> Iterable[str]:
        key: str
        for key in self._data.keys():
            yield key

    def __str__(self) -> str:
        return str(dict(self))
