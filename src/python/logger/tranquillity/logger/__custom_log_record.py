from datetime import datetime
from dataclasses import dataclass
from typing import Union


@dataclass
class CustomLogRecordException:
    name: str
    filename: str
    line: int
    exception: str


@dataclass
class CustomLogRecord:
    time: datetime
    message: str
    filename: str
    line: int
    level: str
    module: str
    host: str
    exception: Union[CustomLogRecordException, None] = None
