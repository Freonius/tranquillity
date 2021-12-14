

from logging import Logger
from typing import Dict, Union, Type, TypeVar
from .__interface import IConnection
from ._rabbit import Rabbit
from ..settings import KVSetting

T = TypeVar('T', bound=IConnection)


class ConnectionBuilder(object):
    _host: Union[str, None] = None
    _port: Union[int, None] = None
    _user: Union[str, None] = None
    _password: Union[str, None] = None
    _queue: Union[str, None] = None
    _db: Union[str, None]
    _settings: KVSetting = KVSetting()
    _log: Union[Logger, None] = None
    
    def __init__(self, prefix: str, log: Union[Logger, None]) -> None:
        super().__init__()

    @property
    def host(self) -> str:
        if self._host is None:
            raise ValueError
        return self._host

    @host.setter
    def host(self, val: str) -> None:
        self._host = val

    def prepare(self, t: Type[IConnection]) -> None:
        d: Dict[str, Union[str, int]] = {
            'host': self.host,
        }

        raise NotImplementedError
    
    def build(self, t: Type[T]) -> T:
        self.prepare(t)
        return t(self._settings, self._log)
    