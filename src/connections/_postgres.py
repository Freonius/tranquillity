
from typing import Union, Dict
from logging import Logger
from psycopg2 import connect, connection
from ..settings import ISettings
from .__interface import IConnection


class Postgres(IConnection):
    _client: connection

    def __init__(self, settings: Union[ISettings, Dict[str, Union[str, int]], None] = None, log: Union[Logger, None] = None) -> None:
        super().__init__(settings=settings, log=log)
        _data: Dict[str, str] = {
            'host': self._settings.get_ns('conn.postgres.host'),
            'port': self._settings.get_ns('conn.postgres.port'),
            'database': self._settings.get_ns('conn.postgres.db'),
            'user': self._settings.get_ns('conn.postgres.user'),
            'password': self._settings.get_ns('conn.postgres.password')
        }
        self._client = connect(**_data)
