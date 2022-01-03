from pytest import raises
from ._fixture import *


def test_logger(fld):
    from ..tranquillity.logger import CustomLogger, ElasticLogHandler
    from time import sleep
    log = CustomLogger()
    _theres_elastic: bool = False
    for x in log.handlers:
        if isinstance(x, ElasticLogHandler):
            _theres_elastic = True
    assert _theres_elastic is True
    log.info('Hello!')
    sleep(5.)
    assert len(ElasticLogHandler.get_log_record(term='Hello!')) == 1
