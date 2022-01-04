# pylint: disable=invalid-name
from re import match
from datetime import datetime, time, date
from typing import Union


def to_time(t: Union[str, time, datetime]) -> time:
    """Convert a value to time.

    Args:
        t (Union[str, time, datetime]): Value to convert

    Raises:
        ValueError
        TypeError

    Returns:
        time
    """
    if isinstance(t, time):
        return t
    if isinstance(t, str):
        m = match(r'(\d+):(\d+)', t)
        if m is not None:
            hour: int = int(str(m.group(1)))
            minute: int = int(str(m.group(2)))
            return time(hour, minute)
        raise ValueError(f'{t} is not a time format')
    if isinstance(t, datetime):
        return t.time()
    raise TypeError(f'Expected str, time, or datetime, got {type(t)}')


def to_date(s: Union[str, date, datetime]) -> date:
    """Convert a value to a date.

    Args:
        s (Union[str, date, datetime]): Value to convert

    Raises:
        TypeError

    Returns:
        date
    """
    d: date
    if isinstance(s, datetime):
        d = s.date()
    elif isinstance(s, str):
        try:
            d = datetime.strptime(s, '%Y-%m-%d').date()
        except ValueError as v:
            if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                s = s[:-(len(v.args[0]) - 26)]
                d = datetime.strptime(s, '%Y-%m-%d').date()
            else:
                raise
    elif isinstance(s, date):
        d = s
    else:
        raise TypeError(f'Expected str, time, or datetime, got {type(s)}')
    return d
