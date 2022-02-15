from typing import Union, List, Type
from logging import Logger
from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.auth import GoogleOAuth2Mixin, OpenIdMixin
from ..settings.__interface import ISettings
from ..settings._yaml import Yaml
from ..logger._custom_logger import CustomLogger
from ..data._dataobject import DataObject


class Api:
    _settings: ISettings
    _log: Logger
    _entities: List[Type[DataObject]] = []
    _port: int

    def __init__(self, settings: Union[ISettings, None] = None, log: Union[Logger, None] = None) -> None:
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

    def add_entity(self, entity: Type[DataObject]) -> 'Api':
        self._entities.append(entity)
        return self

    def start(self) -> None:
        _app = Application([x.to_api() for x in self._entities])
        _app.listen(self._port)
        IOLoop.current().start()

    def stop(self) -> None:
        IOLoop.current().stop()
