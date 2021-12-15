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
            json_list: List[str] = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                                        :-1]).lower().strip() not in {'package'}),  glob(cwd + sep + '*.json')))
            if len(json_list) == 0:
                raise Exception
            if len(json_list) == 1:
                json_file = json_list[0]
            else:
                json_list_check: List[str] = ['.'.join(basename(x).split('.')[
                    :-1]).lower().strip() for x in json_list]
                if 'tranquillity' in json_list_check:
                    json_file = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                        :-1]).lower().strip() in {'tranquillity'}), json_list))[0]
                elif 'settings' in json_list_check:
                    json_file = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                        :-1]).lower().strip() in {'settings'}), json_list))[0]
                else:
                    raise Exception
        json_file = abspath(json_file)
        if not exists(json_file) or not isfile(json_file):
            raise Exception
        _d: Dict[str, Any] = {}
        with open(json_file) as fh:
            _d = loads(fh.read())
        self._config(_d, defaults=defaults,
                     raise_on_missing=raise_on_missing,
                     read_only=read_only)

    def _update(self, key: str, val: str) -> None:
        pass  # TODO: Update json
