from .__interfaces import ILogHandler
from .__custom_log_record import CustomLogRecord


class SqlLogHandler(ILogHandler):
    _table: str

    def create_folder(self) -> None:
        pass

    def _custom_emit(self, record: CustomLogRecord) -> None:
        # TODO
        _query: str = f'''
        --sql
        INSERT INTO {self._table} (
            log_time,
            log_message,
            log_filename,
            log_line,
            log_level,
            log_module,
            log_host,
            log_exception
        ) VALUES ();
        '''
