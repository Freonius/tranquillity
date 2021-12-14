from os import environ, getcwd, sep
from glob import glob
from os.path import exists, isfile, abspath, basename
from typing import Any, Dict, List, Union
from yaml import load
from yaml.loader import SafeLoader
from .__interface import ISettings


class Yaml(ISettings):
    def __init__(self, yaml_file: Union[str, None] = None) -> None:
        super().__init__()
        if yaml_file is None:
            cwd: str = environ['WORKING_DIR'] if 'WORKING_DIR' in environ.keys(
            ) else getcwd()
            yaml_list: List[str] = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                                        :-1]).lower().strip() not in {'docker-compose', 'pubspec'}),  glob(cwd + sep + '*.y*ml')))
            if len(yaml_list) == 0:
                raise Exception
            if len(yaml_list) == 1:
                yaml_file = yaml_list[0]
            else:
                yaml_list_check: List[str] = ['.'.join(basename(x).split('.')[
                    :-1]).lower().strip() for x in yaml_list]
                if 'tranquillity' in yaml_list_check:
                    yaml_file = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                        :-1]).lower().strip() in {'tranquillity'}), yaml_list))[0]
                elif 'settings' in yaml_list_check:
                    yaml_file = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                        :-1]).lower().strip() in {'settings'}), yaml_list))[0]
                else:
                    raise Exception
        yaml_file = abspath(yaml_file)
        if not exists(yaml_file) or not isfile(yaml_file):
            raise Exception
        _d: Dict[str, Any] = {}
        with open(yaml_file) as fh:
            _d = load(fh.read(), SafeLoader)
        self._config(_d, raise_on_missing=True)

    def _update(self, key: str, val: str) -> None:
        pass  # TODO: Update
