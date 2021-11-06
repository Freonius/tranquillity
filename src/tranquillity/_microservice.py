from typing import Dict, Type, Union
from .interfaces import IConnection, IDBObject, ISettings


class MicroService(object):
    _connections: Dict[str, IConnection] = {}
    _structures: Dict[str, Type[IDBObject]] = {}
    _debug: bool = __debug__

    def __init__(self, name: str, settings: Union[str, ISettings]) -> None:
        self._initialize_settings()
        self._initialize_folders()
        self._initialize_loggers()
        self._test_connections()
        self._test_tables()
        self._create_tables()
        self._migrate()
        self._initialize_blueprints()

    def _initialize_folders(self) -> None:
        pass

    def _initialize_settings(self) -> None:
        pass

    def _cron_jobs(self) -> None:
        pass

    def _watch_settings_changes(self) -> None:
        pass

    def _initialize_loggers(self) -> None:
        pass

    def _test_connections(self) -> None:
        pass

    def _initialize_blueprints(self) -> None:
        pass

    def _test_tables(self) -> None:
        pass

    def _create_tables(self) -> None:
        pass

    def _migrate(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass
