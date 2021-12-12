from os import environ
from typing import Any, Dict, List, Union
from .__interface import ISettings


class Env(ISettings):
    def __init__(self,
                 defaults: Union[Dict[str, Any], None] = None,
                 raise_on_missing: bool = True,
                 read_only: bool = False) -> None:
        self._config(data=dict(environ), defaults=defaults,
                     raise_on_missing=raise_on_missing, read_only=read_only)

    def _update(self, key: str, val: str) -> None:
        environ[key.upper()] = val

    @property
    def path(self) -> List[str]:
        return str(self.get('path', '')).split(';')


class Ini(ISettings):
    def __init__(self) -> None:
        super().__init__()


class Yaml(ISettings):
    def __init__(self) -> None:
        super().__init__()


class Sqlite(ISettings):
    def __init__(self) -> None:
        super().__init__()


class Properties(ISettings):
    def __init__(self) -> None:
        super().__init__()


class Json(ISettings):
    def __init__(self) -> None:
        super().__init__()


class SpringConfig(ISettings):
    def __init__(self) -> None:
        super().__init__()


class KVSetting(ISettings):
    def __init__(self) -> None:
        super().__init__()
        self._config({})

    def _update(self, key: str, val: str) -> None:
        pass