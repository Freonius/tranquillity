'''
Module for the connection interface.
'''
from typing import Dict, Type, Union
from logging import Logger
from types import TracebackType
from abc import ABC, abstractmethod
from tranquillity.settings import ISettings, Yaml, KVSetting


class IConnection(ABC):
    '''
    Interface class for database connection.
    '''
    _settings: ISettings
    _log: Union[None, Logger] = None

    def __init__(self,
                 settings: Union[ISettings,
                                 Dict[str, Union[str, int]], None] = None,
                 log: Union[Logger, None] = None) -> None:
        self.parameters(settings)
        if log is not None:
            self.logger(log)

    def parameters(self,
                   settings: Union[ISettings, Dict[str, Union[str, int]], None] = None) -> None:
        '''
        Set the parameters for the connection.
        '''
        if isinstance(settings, ISettings):
            self._settings = settings
            return
        elif isinstance(settings, dict):
            self._settings = KVSetting(settings)
            return
        elif settings is None:
            self._settings = Yaml()
            return
        raise TypeError(
            f'Expected ISettings, dict, or None type, got {type(settings)}')

    def logger(self, log: Logger) -> None:
        '''
        Set a logger.
        '''
        if not isinstance(log, Logger):
            raise TypeError(f'Expected Logger, got {type(log)}')
        self._log = log

    def _log_debug(self, msg: str) -> None:
        if self._log is not None:
            self._log.debug(msg)

    def _log_info(self, msg: str) -> None:
        if self._log is not None:
            self._log.info(msg)

    def _log_warn(self, msg: str) -> None:
        if self._log is not None:
            self._log.warning(msg)

    def _log_err(self, msg: str) -> None:
        if self._log is not None:
            self._log.error(msg)

    def _log_excp(self, ex: Exception) -> None:
        if self._log is not None:
            self._log.exception(ex)

    def __enter__(self) -> 'IConnection':
        self.connect()
        return self

    def __exit__(self,
                 exception_type: Union[Type[Exception], None],
                 exception_value: Union[Exception, None],
                 exception_traceback: Union[TracebackType, None]) -> None:
        if exception_type is not None and \
                exception_value is not None and \
                exception_traceback is not None:
            self._log_err(f'Got exception of type: {exception_type}')
            self._log_excp(exception_value)
        self.close()

    @property
    def is_connected(self) -> bool:
        '''
        Property indicating whether the client is connected to the database.
        '''
        return self._is_connected()

    @abstractmethod
    def connect(self) -> None:
        '''
        Connect to db.
        '''

    @abstractmethod
    def close(self) -> None:
        '''
        Close the connection to the db.
        '''

    @abstractmethod
    def _is_connected(self) -> bool:
        '''
        Check whether it is connected to the database.
        '''

    # TODO: Add execute_statement method.
