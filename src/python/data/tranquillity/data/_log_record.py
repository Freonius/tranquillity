from datetime import datetime
from typing import Dict, Any
from .__interface import IDBObject
from ..schemas import CustomLogRecordSchema
from ._log_exception import CustomLogRecordException


class CustomLogRecord(IDBObject):
    __table__ = 'bb_logs'
    __schema__ = CustomLogRecordSchema

    def load(self, data: Dict[str, Any]) -> None:
        return super().load(data)

    @property
    def time(self) -> datetime:
        return self._d['time']

    @time.setter
    def time(self, val: datetime) -> None:
        self._d['time'] = val

    @property
    def message(self) -> str:
        return self._d['message']

    @message.setter
    def message(self, val: str) -> None:
        self._d['message'] = val

    @property
    def filename(self) -> str:
        return self._d['filename']

    @filename.setter
    def filename(self, val: str) -> None:
        self._d['filename'] = val

    @property
    def level(self) -> str:
        return self._d['level']

    @level.setter
    def level(self, val: str) -> None:
        self._d['level'] = val

    @property
    def module(self) -> str:
        return self._d['module']

    @module.setter
    def module(self, val: str) -> None:
        self._d['module'] = val

    @property
    def line(self) -> int:
        return self._d['line']

    @line.setter
    def line(self, val: int) -> None:
        self._d['line'] = val

    @property
    def exception(self) -> CustomLogRecordException:
        return CustomLogRecordException(self._d['exception'])

    @exception.setter
    def exception(self, val: CustomLogRecordException) -> None:
        if not val.is_valid:
            raise ValueError('exception is not valid')
        self._d['exception'] = val.serialized
