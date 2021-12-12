'''
Interface for different kind of settings.
'''
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Set, Tuple, Union
from ..exceptions import NotAllowedOperation, ConversionError
from ..conversions._dict import flatten_dict


class ISettings(ABC):
    '''
    Interface class for all settings.
    '''
    _data: Dict[str, str] = {}
    _raise_on_missing: bool = True
    _defaults: Union[Dict[str, str], None] = None
    _read_only: bool = False

    def _config(self,
                data: Dict[str, Any],
                defaults: Union[Dict[str, Any], None] = None,
                required_fields: Union[List[str], Set[str], None] = None,
                raise_on_missing: bool = True,
                read_only: bool = False):
        if defaults is not None and isinstance(defaults, dict):
            self._defaults = flatten_dict(defaults)
        elif defaults is not None:
            if __debug__:
                raise TypeError(
                    f'defaults must be of type None or dict, got {type(defaults)}')
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
            self._read_only = False if str(read_only).lower() in {
                'f', 'false', 'n', 'no'} else True
        else:
            if __debug__:
                raise TypeError(
                    f'read_only must be of type bool, got {type(read_only)}')
            else:
                raise TypeError('read_only must be of type bool')

        if raise_on_missing is not None and isinstance(raise_on_missing, bool):
            self._raise_on_missing = raise_on_missing
        elif raise_on_missing is None:
            self._raise_on_missing = False
        else:
            self._raise_on_missing = True

        if not isinstance(data, dict):
            raise TypeError('data must be of type dict')

        self._data = flatten_dict(data)

        if required_fields is not None and \
                isinstance(required_fields, (list, set)) and len(required_fields) > 0:
            key: str
            for key in required_fields:
                key = key.lower().strip()
                if key not in self._data.keys() or \
                        (self._defaults is not None and key not in self._defaults.keys()):
                    raise KeyError(f'key "{key}" missing')
            del key

    def __getitem__(self, key: str) -> Union[str, None]:
        return self.get(key=key, default=None)

    def __setitem__(self, key: str, val: str) -> None:
        self.set(key=key, val=val)

    def get(self, key: str, default: Union[str, None] = None) -> Union[str, None]:
        '''
        Find the value given a key.
        '''
        if not isinstance(key, str):
            raise TypeError(f'key must be of type str, got {type(key)}')
        key = key.lower()
        if key not in self._data.keys():
            if default is not None:
                if isinstance(default, str):
                    return default
                raise TypeError(
                    f'default value must be of type str, got {type(default)}')
            elif self._defaults is not None:
                if key in self._defaults.keys():
                    return self._defaults[key]
                elif self._raise_on_missing:
                    raise KeyError(f'key "{key}" not found')
            elif self._raise_on_missing:
                raise KeyError(f'key "{key}" not found')
            return None
        return self._data[key]

    def get_ns(self, key: str) -> str:
        val: Union[str, None] = self.get(key)
        if val is None:
            raise KeyError
        return val

    def set(self, key: str, val: str) -> None:
        '''
        Set or update a value.
        '''
        if self._read_only:
            raise NotAllowedOperation(f'{type(self)} was marked as read only')
        if not isinstance(key, str):
            raise TypeError(f'key must be of type str, got {type(key)}')
        if not isinstance(val, str):
            raise TypeError(f'val must be of type str, got {type(val)}')
        key = key.lower()
        self._data[key] = val
        self._update(key, val)

    def get_int(self, key: str, default: Union[int, None] = None) -> Union[int, None]:
        '''
        Get a value as an int.
        '''
        if default is not None and not isinstance(default, int):
            raise TypeError('default must be of type int')
        tmp: Union[str, None] = self.get(
            key, str(default) if default is not None else None)
        if tmp is None:
            return None
        try:
            return int(tmp)
        except ValueError as ex:
            raise ConversionError(f'Could not convert "{tmp}" to int') from ex

    def get_float(self, key: str, default: Union[float, None] = None) -> Union[float, None]:
        '''
        Get a value as a float.
        '''
        if default is not None and not isinstance(default, float):
            raise TypeError('default must be of type float')
        tmp: Union[str, None] = self.get(
            key, str(default) if default is not None else None)
        if tmp is None:
            return None
        try:
            return float(tmp)
        except ValueError as ex:
            raise ConversionError(
                f'Could not convert "{tmp}" to float') from ex

    def get_bool(self, key: str, default: Union[bool, None] = None) -> bool:
        '''
        Get a value as a bool.
        '''
        if default is not None and not isinstance(default, float):
            raise TypeError('default must be of type float')
        tmp: Union[str, None] = self.get(
            key, str(default) if default is not None else None)
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

    def get_int_ns(self, key: str) -> int:
        val: Union[int, None] = self.get_int(key)
        if val is None:
            raise KeyError
        return val

    def get_float_ns(self, key: str) -> float:
        val: Union[float, None] = self.get_float(key)
        if val is None:
            raise KeyError
        return val

    def lookup(self,
               keys: Union[List[str], Set[str], Tuple[str, ...]],
               default: Union[str, None] = None) -> Union[str, None]:
        '''
        Find a value in a set of keys.
        '''
        if not isinstance(keys, (list, set, tuple)):
            raise TypeError('keys must be fo type list')
        if default is not None and not isinstance(default, str):
            raise TypeError('default must be of type str or None')
        if len(keys) == 0:
            pass
        _old_raise: bool = self._raise_on_missing
        self._raise_on_missing = True
        key: str
        val: Union[str, None] = None
        for key in keys:
            try:
                val = self.get(key)
                break
            except KeyError:
                continue
        try:
            del key
        except NameError:
            pass
        self._raise_on_missing = _old_raise
        del _old_raise
        if val is None:
            if default is None and self._raise_on_missing:
                raise KeyError(f'keys {keys} not found')
            else:
                return default
        return val

    def lookup_ns(self, keys: Union[List[str], Set[str], Tuple[str, ...]]) -> str:
        val: Union[str, None] = self.lookup(keys)
        if val is None:
            raise KeyError
        return val

    def __iter__(self) -> Iterable[Tuple[str, str]]:
        key: str
        val: str
        for key, val in self._data.items():
            yield key, val

    def keys(self) -> Iterable[str]:
        '''
        Returns all the keys in the settings.
        '''
        key: str
        for key in self._data.keys():
            yield key

    def __str__(self) -> str:
        return str(dict(self))

    @abstractmethod
    def _update(self, key: str, val: str) -> None:
        pass
