from os import sep
from sys import stdout
from logging import DEBUG, INFO, ERROR, WARNING, LogRecord, Logger, StreamHandler, getLoggerClass, Formatter, FileHandler
from typing import List, Union, Dict
from datetime import datetime
from traceback import FrameSummary, StackSummary, extract_tb
from sqlalchemy.sql import text
from flask import Flask
from ..elasticsearch.conn import Elastic
from ..mongo.conn import Mongo
from ..enums import LogType
from ..connections._rabbit import Rabbit
from ..sql import client as sql_client
from ..settings.__interface import ISettings
from ..settings import Env
from ..interfaces import ILogHandler
from ..objects.classes import CustomLogRecord
from tranquillity.shell import Shell


# filterwarnings('ignore')


class CustomLogger(Logger):
    _settings: ISettings

    def __init__(self, name_log_file: str, module_name: str, frmt: Union[str, None] = None, level: int = DEBUG, settings: Union[ISettings, None] = None):
        if level is DEBUG and not __debug__:
            level = INFO
        if frmt is None:
            self.frmt = '[{}@{}'.format(
                module_name, Shell.get_docker_id()) + ':%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s'
        else:
            self.frmt = frmt
        if settings is None:
            settings = Env()
        self._settings = settings
        self.level = level
        self.name_log_file = name_log_file
        self.module_name = module_name
        self.output = {DEBUG: '', INFO: '', ERROR: '', WARNING: ''}
        self.formatter = Formatter(self.frmt)
        super().__init__(name=name_log_file, level=level)

    def add_custom_handler(self, tipo: LogType, level: Union[int, None] = None, override_name: Union[str, None] = None):
        if tipo is LogType.STREAM:
            console_logger = StreamHandler(stdout)
        elif tipo is LogType.ELASTIC:
            console_logger = elastic_log_handler(
                self.module_name, self._settings)
        # elif tipo is LogType.MONGO:
        #     console_logger = mongo_log_handler(
        #         self.module_name, self._settings)
        elif tipo is LogType.SQL:
            console_logger = sql_log_handler(self.module_name, self._settings)
        elif tipo is LogType.FILE:
            if override_name is None:
                console_logger = FileHandler(self.name_log_file)
            else:
                console_logger = FileHandler(override_name)
        elif tipo is LogType.RABBITMQ:
            console_logger = rabbit_log_handler(
                self.module_name, self._settings)
        else:
            return
        if level is None:
            console_logger.setLevel(self.level)
        else:
            console_logger.setLevel(level)
        console_logger.setFormatter(self.formatter)
        self.addHandler(console_logger)


class elastic_log_handler(ILogHandler):
    def _custom_emit(self, record: CustomLogRecord) -> None:
        es = Elastic(self._settings)
        es.add(record)
        es.close()


# class mongo_log_handler(ILogHandler):
#     def _custom_emit(self, record: CustomLogRecord) -> None:
#         m = Mongo(self._settings)
#         m.add(record)
#         m.close()


class rabbit_log_handler(ILogHandler):
    def _custom_emit(self, record: CustomLogRecord) -> None:
        r = Rabbit(record.get_table(), self._settings)
        r.send(record)
        r.close()


def rabbit_log_listener(record: CustomLogRecord, r: Rabbit):
    es_log: bool
    mongo_log: bool
    settings = r._settings
    try:
        es_log = str(settings['log.elasticsearch']
                     ).strip().lower() in {'true', '1'}
    except Exception:
        es_log = False
    try:
        mongo_log = str(settings['log.mongo']).strip().lower() in {'true', '1'}
    except Exception:
        mongo_log = False
    if mongo_log:
        m = Mongo(settings)
        m.add(record)
        m.close()
    if es_log:
        es = Elastic(settings)
        es.add(record)
        es.close()


class sql_log_handler(StreamHandler):
    _module_name: str = ''
    _settings: ISettings

    def __init__(self, module_name: str, settings: ISettings):
        self._module_name = module_name
        self._settings = settings
        super().__init__(stdout)

    def emit(self, record: LogRecord):

        log_doc: Dict[str, Union[None, str, int, datetime, Dict[str, Union[str, int]]]] = {
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
                frame_summaries: List[FrameSummary] = [
                    frame_summary for frame_summary in stack_summary]
                if len(frame_summaries) > 0:
                    frm_sum: FrameSummary = frame_summaries[-1]
                    log_doc['exception'] = str({
                        'name': frm_sum.name,
                        'filename': frm_sum.filename,
                        'line': frm_sum.lineno,
                        'exception': record.exc_info[1].__class__.__name__
                    })
        if 'exception' not in log_doc.keys():
            log_doc['exception'] = None
        query = text('''INSERT INTO bb_logs.logs (
                                            log_time,
                                            log_message,
                                            log_filename,
                                            log_line,
                                            log_level,
                                            log_module,
                                            log_exception)
                                        VALUES (
                                            :time,
                                            :message,
                                            :filename,
                                            :line,
                                            :level:
                                            :module,
                                            :exception
                                        );''')
        with sql_client(self._settings) as sql:
            sql.execute(query, **log_doc)


def logger(module_name: Union[str, None] = None, settings: Union[ISettings, None] = None) -> CustomLogger:
    if settings is None:
        settings = IniFile()
    if module_name is None:
        module_name = str(settings['log.module'])
    log_path: str = settings['log.path']
    if log_path is None:
        log_path = ''
    if log_path.strip() == '':
        log_path = '.'
    if not log_path.endswith(sep):
        log_path += sep
    mylogger = CustomLogger(log_path + module_name.lower().replace(
        ' ', '_').strip() + '.log', module_name, settings=settings)
    if __debug__:
        mylogger.add_custom_handler(LogType.STREAM, DEBUG)
        mylogger.add_custom_handler(
            LogType.FILE, DEBUG, log_path + 'debug.log')
    else:
        mylogger.add_custom_handler(LogType.STREAM, INFO)
        mylogger.add_custom_handler(
            LogType.FILE, INFO, log_path + 'debug.log')
    mylogger.add_custom_handler(
        LogType.FILE, WARNING, log_path + 'errors.log')
    es_log: bool
    mongo_log: bool
    rabbit_log: bool
    try:
        es_log = str(settings['log.elasticsearch']
                     ).strip().lower() in {'true', '1'}
    except Exception:
        es_log = False
    try:
        mongo_log = str(settings['log.mongo']).strip().lower() in {'true', '1'}
    except Exception:
        mongo_log = False
    try:
        rabbit_log = str(settings['log.rabbit']
                         ).strip().lower() in {'true', '1'}
    except Exception:
        rabbit_log = False
    if es_log:
        mylogger.add_custom_handler(LogType.ELASTIC, INFO)
    # if mongo_log:
    #     mylogger.add_custom_handler(LogType.MONGO, INFO)
    if rabbit_log:
        mylogger.add_custom_handler(LogType.RABBITMQ)

    return mylogger
