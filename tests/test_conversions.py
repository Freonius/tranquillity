from datetime import datetime, time, date
from pytest import raises


def test_bool():
    from ..src.utils import to_bool
    with raises(TypeError):
        to_bool({})
    trues = [
        to_bool(True),
        to_bool('1'),
        to_bool(1),
        to_bool(1.),
        to_bool('true'),
    ]
    falses = [
        to_bool(False),
        to_bool('0'),
        to_bool(0),
        to_bool(0.5),
        to_bool('false'),
        to_bool('error'),
        to_bool(None),
    ]
    for t in trues:
        assert t is True
        assert isinstance(t, bool)
    for f in falses:
        assert f is False
        assert isinstance(f, bool)


def test_time():
    from ..src.utils import to_time
    assert isinstance(to_time(time(10, 20)), time)
    assert isinstance(to_time(datetime.now()), time)
    assert isinstance(to_time('10:20'), time)
    t = time(10, 20)
    c = to_time('10:20')
    assert t.hour == c.hour
    assert t.minute == c.minute
    with raises(ValueError):
        to_time('not a time format')
    with raises(TypeError):
        to_time({})


def test_date():
    from ..src.utils import to_date
    assert to_date('2022-07-25') == date(2022, 7, 25)
    assert to_date('2022-07-25 00:00:00') == date(2022, 7, 25)
    assert to_date(date(2022, 7, 25)) == date(2022, 7, 25)
    assert to_date(datetime.now()) == date.today()
    with raises(TypeError):
        to_date({})
    with raises(ValueError):
        to_date('not a valid string')
