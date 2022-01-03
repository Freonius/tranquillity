from datetime import datetime
from abc import ABC, abstractmethod
from sys import stdout
from logging import LogRecord, StreamHandler
from typing import List, Union
from traceback import FrameSummary, StackSummary, extract_tb
from tranquillity.settings import ISettings
from tranquillity.shell import Shell
from .__custom_log_record import CustomLogRecord, CustomLogRecordException


class ILogHandler(StreamHandler, ABC):
    _module_name: str = ''
    _host: str = ''
    _settings: ISettings

    def __init__(self, settings: ISettings):
        self._module_name = settings.get_ns('app.name')
        self._settings = settings
        self._host = Shell.get_docker_id()
        super().__init__(stdout)

    def emit(self, record: LogRecord):

        _e: Union[CustomLogRecordException, None] = None

        if record.levelname == 'ERROR':
            if record.exc_info is None:
                pass
                # Is error, not exception
            else:
                stack_summary: StackSummary = extract_tb(record.exc_info[2])
                frame_summaries: List[FrameSummary] = list(stack_summary)
                if len(frame_summaries) > 0:
                    frm_sum: FrameSummary = frame_summaries[-1]

                    _e = CustomLogRecordException(
                        name=frm_sum.name,
                        filename=frm_sum.filename,
                        line=frm_sum.lineno,
                        exception=record.exc_info[1].__class__.__name__,
                    )
        _c: CustomLogRecord = CustomLogRecord(
            time=datetime.fromtimestamp(record.created),
            message=record.message,
            filename=record.filename,
            level=record.levelname,
            module=self._module_name,
            line=record.lineno,
            host=self._host,
            exception=_e
        )
        self._custom_emit(_c)

    @abstractmethod
    def _custom_emit(self, record: CustomLogRecord) -> None:
        pass
