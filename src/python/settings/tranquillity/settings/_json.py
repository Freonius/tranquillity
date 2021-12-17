from os import environ, getcwd, sep
from glob import glob
from os.path import exists, isfile, abspath, basename
from typing import Any, Dict, List, Union
from json import loads
from .__interface import ISettings


class Json(ISettings):
    def __init__(self, json_file: Union[str, None] = None,
                 defaults: Union[Dict[str, Any], None] = None,
                 raise_on_missing: bool = True,
                 read_only: bool = False) -> None:
        super().__init__()
        if json_file is None:
            cwd: str = environ['WORKING_DIR'] if 'WORKING_DIR' in environ.keys(
            ) else getcwd()
            _json_list: List[str] = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                :-1]).lower().strip() not in {'package'}),  glob(cwd + sep + '*.json')))
            if len(_json_list) == 0:
                raise Exception('No json file found')
            if len(_json_list) == 1:
                json_file = _json_list[0]
            else:
                _json_list_check: List[str] = ['.'.join(basename(x).split('.')[
                    :-1]).lower().strip() for x in _json_list]
                if 'tranquillity' in _json_list_check:
                    json_file = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                        :-1]).lower().strip() in {'tranquillity'}), _json_list))[0]
                elif 'settings' in _json_list_check:
                    json_file = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                        :-1]).lower().strip() in {'settings'}), _json_list))[0]
                else:
                    raise Exception('I found more than one json file')
                del _json_list_check
            del _json_list
        json_file = abspath(json_file)
        if not exists(json_file) or not isfile(json_file):
            raise Exception(f'The file {json_file} does not exist')
        _d: Dict[str, Any] = {}
        with open(json_file) as fh:
            _d = loads(fh.read())
        del json_file
        self._config(_d, defaults=defaults,
                     raise_on_missing=raise_on_missing,
                     read_only=read_only)

    def _update(self, key: str, val: str) -> None:
        pass  # TODO: Update json
