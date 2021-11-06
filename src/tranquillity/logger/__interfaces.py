from logging import StreamHandler, LogRecord
from abc import ABC, abstractmethod
from typing import Dict

class ILogHandler(ABC, StreamHandler):
    def emit(self, record: LogRecord) -> None:
        return super().emit(record)

    @abstractmethod
    def _emit(self, data: Dict[str, str]) -> None:
        pass
