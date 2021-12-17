from os import environ, getcwd, sep
from glob import glob
from os.path import exists, isfile, abspath, basename
from typing import Any, Dict, List, Union
from yaml import load
from yaml.loader import SafeLoader
from .__interface import ISettings


class Yaml(ISettings):
    def __init__(self, yaml_file: Union[str, None] = None,
                 defaults: Union[Dict[str, Any], None] = None,
                 raise_on_missing: bool = True,
                 read_only: bool = False) -> None:
        super().__init__()
        if yaml_file is None:
            cwd: str = environ['WORKING_DIR'] if 'WORKING_DIR' in environ.keys(
            ) else getcwd()
            yaml_list: List[str] = list(filter(lambda x: ('.'.join(basename(x).split('.')[
                                        :-1]).lower().strip() not in {'docker-compose', 'pubspec'}),  glob(cwd + sep + '*.y*ml')))
            if len(yaml_list) == 0:
                raise Exception('No yaml file provided or found')
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
                    raise Exception('I found more than one yaml file')
                del yaml_list_check
            del yaml_list
        yaml_file = abspath(yaml_file)
        if not exists(yaml_file) or not isfile(yaml_file):
            raise Exception(f'The file {yaml_file} does not exist')
        _d: Dict[str, Any] = {}
        with open(yaml_file) as fh:
            _d = load(fh.read(), SafeLoader)
        del yaml_file
        self._config(_d, defaults=defaults,
                     raise_on_missing=raise_on_missing,
                     read_only=read_only)

    def _update(self, key: str, val: str) -> None:
        pass  # TODO: Update
