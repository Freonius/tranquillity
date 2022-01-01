# pylint: disable=duplicate-code
# mypy: ignore-errors
'''
Interface for different kind of settings.
'''
from os import environ, getcwd, sep
from os.path import exists, isfile, abspath, basename
from glob import glob
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Set, Tuple, Union
from ast import literal_eval
# pylint: disable=no-name-in-module,import-error
from tranquillity.exceptions import NotAllowedOperation, ConversionError
from tranquillity.utils import flatten_dict, to_bool
# pylint: enable=no-name-in-module,import-error


class ISettings(ABC):
    '''
    Interface class for all settings.
    '''
    _data: Dict[str, str] = {}
    _raise_on_missing: bool = True
    _defaults: Union[Dict[str, str], None] = None
    _read_only: bool = False

    # pylint: disable=too-many-arguments
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
            raise TypeError('defaults must be of type None or dict')
        # read_only
        self._read_only = to_bool(read_only)

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
    # pylint: enable=too-many-arguments

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
            if self._defaults is not None:
                if key in self._defaults.keys():
                    return self._defaults[key]
                raise KeyError(f'key "{key}" not found')
            if self._raise_on_missing:
                raise KeyError(f'key "{key}" not found')
            return None
        return self._data[key]

    def get_ns(self, key: str) -> str:
        val: Union[str, None] = self.get(key)
        if val is None:
            raise KeyError
        return val

    def get_eval(self, key: str) -> Any:
        _v: Union[str, None] = self.get(key)
        if _v is None:
            return _v
        try:
            return literal_eval(_v)
        except ValueError:
            return _v

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
        if default is not None and not isinstance(default, bool):
            raise TypeError('default must be of type bool')
        tmp: Union[str, None] = self.get(
            key, str(default) if default is not None else None)
        return bool(to_bool(tmp))

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
            return default
        return val

    def lookup_ns(self, keys: Union[List[str], Set[str], Tuple[str, ...]],
                  default: Union[str, None] = None) -> str:
        val: Union[str, None] = self.lookup(keys, default)
        if val is None:
            raise KeyError
        return val

    def lookup_int(self, keys: Union[List[str], Set[str], Tuple[str, ...]],
                   default: Union[int, None] = None) -> Union[int, None]:
        val: Union[str, None] = self.lookup(keys)
        if default is not None and not isinstance(default, int):
            raise TypeError
        if val is None:
            return default
        return int(val)

    def lookup_int_ns(self, keys: Union[List[str], Set[str], Tuple[str, ...]],
                      default: Union[int, None] = None) -> int:
        val: Union[int, None] = self.lookup_int(keys, default)
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

    @staticmethod
    def _get_file_name(file_name: Union[str, None], extension: str) -> str:
        exclusions: Set[str] = {}
        extension = extension.strip().lower()
        if extension in {'yml', 'yaml'}:
            extension = 'y*ml'
            exclusions = {'docker-compose', 'pubspec'}
        elif extension == 'ini':
            extension = 'ini'
            exclusions = {}
        elif extension == 'json':
            extension = 'json'
            exclusions = {'package'}
        if file_name is None:
            cwd: str = environ['WORKING_DIR'] if 'WORKING_DIR' in environ.keys(
            ) else getcwd()
            file_list: List[str] = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                                        :-1]).lower().strip() not in exclusions),
                glob(cwd + sep + f'*.{extension}')))
            if len(file_list) == 0:
                raise Exception(f'No {extension} file provided or found')
            if len(file_list) == 1:
                file_name = file_list[0]
            else:
                file_list_check: List[str] = ['.'.join(basename(x).split('.')[
                    :-1]).lower().strip() for x in file_list]
                if 'tranquillity' in file_list_check:
                    file_name = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                        :-1]).lower().strip() in {'tranquillity'}), file_list))[0]
                elif 'settings' in file_list_check:
                    file_name = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                        :-1]).lower().strip() in {'settings'}), file_list))[0]
                else:
                    raise Exception(f'I found more than one {extension} file')
                del file_list_check
            del file_list
        file_name = abspath(file_name)
        if not exists(file_name) or not isfile(file_name):
            raise Exception(f'The file {file_name} does not exist')
        return file_name

    @abstractmethod
    def _update(self, key: str, val: str) -> None:
        pass
