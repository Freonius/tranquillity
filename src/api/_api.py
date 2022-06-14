from typing import Tuple, Union, List, Type, Dict
from logging import Logger
from types import NotImplementedType, TracebackType
from abc import ABC, abstractmethod
from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.auth import GoogleOAuth2Mixin, OpenIdMixin
import nest_asyncio
from ..settings.__interface import ISettings
from ..settings._yaml import Yaml
from ..logger._custom_logger import CustomLogger
from ..data._dataobject import DataObject
from ..connections.__interface import IConnection
from ._user import User


class Api(ABC):
    _settings: ISettings
    _log: Logger
    _entities: List[Type[DataObject]] = []
    _port: int
    _loop: Union[IOLoop, None] = None
    _token_key: Union[str, List[str], None] = None
    _default_connection: Union[IConnection, Type[IConnection], None] = None

    def __init__(self, *, default_connection: Union[IConnection, Type[IConnection], None] = None, token_key: Union[str, List[str], None] = None, user: Union[Type[User], None] = None, settings: Union[ISettings, None] = None, log: Union[Logger, None] = None) -> None:
        if settings is None:
            settings = Yaml()
        self._settings = settings
        if log is None:
            log = CustomLogger(settings)
        self._log = log
        _port: int = 8888
        try:
            _port = self._settings.get_int_ns('app.port')
        except KeyError:
            pass
        self._port = _port
        if user is not None:
            self.add_entity(user)
        self._token_key = token_key
        self._default_connection = default_connection

    @abstractmethod
    def auth(self, header: Dict[str, str], permission: str) -> Tuple[bool, Dict[str, str]]:
        return False, {}

    def add_entity(self, entity: Type[DataObject]) -> 'Api':
        if entity.__conn__ is None:
            entity.__conn__ = self._default_connection
        if entity.__settings__ is None:
            entity.__settings__ = self._settings
        if isinstance(entity.__table__, NotImplementedType):
            entity.__table__ = entity.__name__.lower()
        self._entities.append(entity)
        return self

    def start(self) -> None:
        _app = Application([x.to_api(
            log=self._log, token_key=self._token_key, auth=self.auth) for x in self._entities])
        _app.listen(self._port)
        nest_asyncio.apply()
        IOLoop.current().start()

    def stop(self) -> None:
        IOLoop.current().stop()

    def __enter__(self) -> 'Api':
        self.start()
        return self

    def __exit__(self,
                 exception_type: Union[Type[Exception], None],
                 exception_value: Union[Exception, None],
                 exception_traceback: Union[TracebackType, None]) -> None:
        if exception_type is not None and \
                exception_value is not None and \
                exception_traceback is not None:
            self._log.error(f'Got exception of type: {exception_type}')
            self._log.exception(exception_value)
        self.stop()
