def test_logger(settings_file):
    from ..src.logger import CustomLogger, ElasticLogHandler
    from datetime import date, datetime
    from logging import INFO, ERROR
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
    assert len(ElasticLogHandler.get_log_record(level=INFO)) == 1
    try:
        1 / 0
    except Exception as e:
        log.exception(e)
    sleep(5.)
    assert len(ElasticLogHandler.get_log_record(level='ERROR')) == 1
    log.error('Oh no!')
    sleep(5.)
    assert len(ElasticLogHandler.get_log_record(level=ERROR)) == 2
    assert len(ElasticLogHandler.get_log_record(date_filter=date.today())) == 3
    assert len(ElasticLogHandler.get_log_record(
        date_filter=datetime.now(), module='Tranquillity', level=7383)) == 0
    assert len(ElasticLogHandler.get_log_record()) == 3
