from datetime import datetime
from abc import ABC, abstractmethod
from sys import stdout
from logging import LogRecord, StreamHandler
from typing import List, Union, Dict
from datetime import datetime
from traceback import FrameSummary, StackSummary, extract_tb
from ..settings.__interface import ISettings
from ..objects.classes import CustomLogRecord


class ILogHandler(StreamHandler, ABC):
    _module_name: str = ''
    _settings: ISettings

    def __init__(self, module_name: str, settings: ISettings):
        self._module_name = module_name
        self._settings = settings
        super().__init__(stdout)

    def emit(self, record: LogRecord):

        log_doc: Dict[str, Union[str, int, datetime, Dict[str, Union[str, int]]]] = {
            'time': datetime.fromtimestamp(record.created),
            'message': record.message,
            'filename': record.filename,
            'line': record.lineno,
            'level': record.levelname,
            'module': self._module_name
        }

        if record.levelname == 'ERROR':
            if record.exc_info is None:
                pass
                # Is error, not exception
            else:
                stack_summary: StackSummary = extract_tb(record.exc_info[2])
                frame_summaries: List[FrameSummary] = [frame_summary for frame_summary in stack_summary]
                if len(frame_summaries) > 0:
                    frm_sum: FrameSummary = frame_summaries[-1]
                    log_doc['exception'] = {
                        'name': frm_sum.name,
                        'filename': frm_sum.filename,
                        'line': frm_sum.lineno,
                        'exception': record.exc_info[1].__class__.__name__
                    }
        self._custom_emit(CustomLogRecord(log_doc))

    @abstractmethod
    def _custom_emit(self, record: CustomLogRecord) -> None:
        pass
    