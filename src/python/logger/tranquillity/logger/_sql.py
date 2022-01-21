from .__interfaces import ILogHandler
from .__custom_log_record import CustomLogRecord


class SqlLogHandler(ILogHandler):

    def _custom_emit(self, record: CustomLogRecord) -> None:
        pass  # TODO
