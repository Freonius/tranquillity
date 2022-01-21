from sys import stdout
from logging import DEBUG, INFO, ERROR, WARNING, Logger, StreamHandler, Formatter, FileHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from os.path import abspath, isdir
from os import makedirs
# pylint: disable=redefined-builtin
from re import compile, Pattern, Match, finditer, match
# pylint: enable=redefined-builtin
from typing import Union
from warnings import filterwarnings
from tranquillity.shell import Shell
from tranquillity.settings import ISettings, Yaml
from ._enum import LogType
from ._elasticlog import ElasticLogHandler
from ._rabbit import RabbitLogHandler
from ._sql import SqlLogHandler

filterwarnings('ignore')


class CustomLogger(Logger):
    _settings: ISettings

    def _calc_level(self, _log_name: str) -> int:
        level: int = DEBUG
        try:
            _val: str = self._settings.get_ns(
                f'log.loggers.{_log_name}.level').upper().strip()
            if _val == 'DEBUG':
                level = DEBUG
            elif _val == 'INFO':
                level = INFO
            elif _val == 'WARNING':  # pragma: no cover
                level = WARNING     # pragma: no cover
            elif _val == 'ERROR':   # pragma: no cover
                level = ERROR       # pragma: no cover
            del _val
        except KeyError:            # pragma: no cover
            pass                    # pragma: no cover
        if level is DEBUG and not __debug__:
            level = INFO    # I am going to be a nazi here
        return level

    def __init__(self, settings: Union[ISettings, None] = None):

        if settings is None:
            settings = Yaml()
        self._settings = settings
        level: int = self._calc_level('file')
        _ptrn: Pattern = compile(r'\{\{\s*([a-z\.]+)\s*\}\}')
        _m: Match
        name_log_file: str = settings.get_ns('log.loggers.file.file')

        for _m in finditer(_ptrn, name_log_file):
            name_log_file = name_log_file.replace(
                _m.group(0), settings.get_ns(_m.group(1)), 1)
            del _m

        del _ptrn

        module_name: str = settings.get_ns('app.name')
        frmt: Union[str, None] = None

        try:
            frmt = settings.get('log.format')
        except KeyError:    # pragma: no cover
            pass            # pragma: no cover

        if frmt is None:
            self.frmt = f'[{module_name}@{Shell.get_docker_id()}' + \
                ':%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s'
        else:
            self.frmt = frmt    # pragma: no cover
        self.level = level
        self.name_log_file = name_log_file
        _log_fld: str = str(Path(abspath(self.name_log_file)).parent)
        if not isdir(_log_fld):
            makedirs(_log_fld)
        self.module_name = module_name
        self.output = {DEBUG: '', INFO: '', ERROR: '', WARNING: ''}
        self.formatter = Formatter(self.frmt)
        super().__init__(name=name_log_file, level=level)
        self._add_custom_handlers(settings)
        self._add_rotation_handler(settings)

    def _add_custom_handlers(self, settings: ISettings) -> None:
        try:
            if settings.get_bool('log.loggers.file.enabled'):
                self.add_custom_handler(LogType.FILE, self._calc_level('file'))
        except KeyError:    # pragma: no cover
            pass            # pragma: no cover
        try:
            if settings.get_bool('log.loggers.stream.enabled'):
                self.add_custom_handler(
                    LogType.STREAM, self._calc_level('stream'))
        except KeyError:    # pragma: no cover
            pass            # pragma: no cover
        try:
            if settings.get_bool('log.loggers.sql.enabled'):
                self.add_custom_handler(LogType.SQL, self._calc_level('sql'))
        except KeyError:    # pragma: no cover
            pass            # pragma: no cover
        try:
            if settings.get_bool('log.loggers.rabbitmq.enabled'):
                self.add_custom_handler(
                    LogType.RABBITMQ, self._calc_level('rabbitmq'))
        except KeyError:    # pragma: no cover
            pass            # pragma: no cover
        try:
            if settings.get_bool('log.loggers.elasticsearch.enabled'):
                self.add_custom_handler(
                    LogType.ELASTIC, self._calc_level('elasticsearch'))
        except KeyError:    # pragma: no cover
            pass            # pragma: no cover

    def _add_rotation_handler(self, settings: ISettings) -> None:
        _rotation_enabled: bool = False
        try:
            if settings.get_bool('log.rotation.enabled'):
                _rotation_enabled = True
        except KeyError:                # pragma: no cover
            _rotation_enabled = False   # pragma: no cover
        _daily: bool = False
        try:
            _daily = settings.get_bool('log.rotation.daily')
        except KeyError:                # pragma: no cover
            _daily = False              # pragma: no cover
        _keep: int = 10
        try:
            _keep = settings.get_int('log.rotation.keep')
        except KeyError:                # pragma: no cover
            _keep = 10                  # pragma: no cover
        try:
            _size: Union[str, None] = settings.get('log.rotation.size')
            _bytes: int = 0
            if _size is not None:
                _size = _size.strip().upper()
                _m_size: Union[Match, None] = match(
                    r'^(\d+)(KB?|MB?)?$', _size)
                del _size
                if _m_size is not None:
                    _digits: int = int(_m_size.group(1))
                    _size_part: str = _m_size.group(2)
                    del _m_size
                    if _size_part in {'K', 'KB'}:
                        _digits *= 1024
                    elif _size_part in {'M', 'MB'}:     # pragma: no cover
                        _digits *= 1024                 # pragma: no cover
                        _digits *= 1024                 # pragma: no cover
                    _bytes = _digits
                    del _digits, _size_part
            if _rotation_enabled and _bytes > 0:
                self.addHandler(
                    RotatingFileHandler(self.name_log_file, backupCount=_keep,
                                        maxBytes=_bytes))
            del _bytes
        except KeyError:    # pragma: no cover
            pass            # pragma: no cover
        if _rotation_enabled and _daily:
            self.addHandler(TimedRotatingFileHandler(
                self.name_log_file, when='d'))

    def add_custom_handler(self,
                           logtype: LogType,
                           level: Union[int, None] = None,):
        console_logger: Union[StreamHandler, ElasticLogHandler,
                              SqlLogHandler, FileHandler, RabbitLogHandler]
        if logtype is LogType.STREAM:
            console_logger = StreamHandler(stdout)
        elif logtype is LogType.ELASTIC:
            console_logger = ElasticLogHandler(self._settings)
        # elif logtype is LogType.MONGO:
        #     console_logger = mongo_log_handler(
        #         self.module_name, self._settings)
        elif logtype is LogType.SQL:
            console_logger = SqlLogHandler(self._settings)
        elif logtype is LogType.FILE:
            console_logger = FileHandler(self.name_log_file)
        elif logtype is LogType.RABBITMQ:
            console_logger = RabbitLogHandler(self._settings)
        else:
            return  # pragma: no cover
        if level is None:
            console_logger.setLevel(self.level)  # pragma: no cover
        else:
            console_logger.setLevel(level)
        console_logger.setFormatter(self.formatter)
        self.addHandler(console_logger)
