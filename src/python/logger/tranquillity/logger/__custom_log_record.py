from datetime import datetime
from dataclasses import dataclass
from logging import LogRecord
from typing import Dict, Union, Any
# pylint: disable=too-many-instance-attributes


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


def _lr2d(log_rec: CustomLogRecord) -> Dict[str, Any]:
    _ex: Union[None, Dict[str, Any]] = None
    if log_rec.exception is not None:
        _ex = {
            'name': log_rec.exception.name,
            'filename': log_rec.exception.filename,
            'line': log_rec.exception.line,
            'exception': log_rec.exception.exception
        }
    return {
        'time': log_rec.time.isoformat(),
        'message': log_rec.message,
        'filename': log_rec.filename,
        'line': log_rec.line,
        'level': log_rec.level,
        'module': log_rec.module,
        'host': log_rec.host,
        'exception': _ex
    }


def _d2lr(hits: Dict[str, Any]) -> CustomLogRecord:
    for _x in ('time', 'message', 'filename', 'line', 'level', 'module', 'host', 'exception'):
        if _x not in hits.keys():
            raise ValueError    # pragma: no cover
    _ex: Union[CustomLogRecordException, None] = None
    if hits['exception'] is not None and isinstance(hits['exception'], dict):
        for _y in ('name', 'filename', 'line', 'exception'):
            if _y not in hits['exception'].keys():
                raise TypeError  # pragma: no cover
        _ex = CustomLogRecordException(**hits['exception'])
    hits.pop('exception')
    hits['exception'] = _ex
    return CustomLogRecord(**hits)
