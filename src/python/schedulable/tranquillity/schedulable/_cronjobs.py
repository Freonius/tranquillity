from typing import Callable, List, Union
from datetime import datetime, time
from time import sleep
from functools import partial
from re import compile, match, Match, Pattern
from threading import Thread
from croniter import CroniterBadCronError, croniter


class CronBit:
    _parent: 'CronBuilder'
    _val: Union[List[int], int]
    _verb: str

    def __init__(self, parent: 'CronBuilder', val: Union[List[int], int], verb: str) -> None:
        self._parent = parent
        self._val = val
        self._verb = verb

    @property
    def minutes(self) -> 'CronBuilder':
        val: str
        if isinstance(self._val, list):
            val = ','.join(list(map(str, self._val)))
        else:
            val = str(self._val)
        if self._verb == 'every':
            val = '*/' + val
        self._parent.minutes = val
        return self._parent

    @property
    def hours(self) -> 'CronBuilder':
        val: str
        if isinstance(self._val, list):
            val = ','.join(list(map(str, self._val)))
        else:
            val = str(self._val)
        if self._verb == 'every':
            val = '*/' + val
        self._parent.hours = val
        return self._parent

    @property
    def days(self) -> 'CronBuilder':
        val: str
        if isinstance(self._val, list):
            val = ','.join(list(map(str, self._val)))
        else:
            val = str(self._val)
        if self._verb == 'every':
            val = '*/' + val
        self._parent.days = val
        return self._parent

    @property
    def months(self) -> 'CronBuilder':
        val: str
        if isinstance(self._val, list):
            val = ','.join(list(map(str, self._val)))
        else:
            val = str(self._val)
        if self._verb == 'every':
            val = '*/' + val
        self._parent.months = val
        return self._parent

    @property
    def weekdays(self) -> 'CronBuilder':
        val: str
        if isinstance(self._val, list):
            val = ','.join(list(map(str, self._val)))
        else:
            val = str(self._val)
        if self._verb == 'every':
            val = '*/' + val
        self._parent.weekdays = val
        return self._parent


class CronBuilder:
    _min: str
    _hour: str
    _day: str
    _month: str
    _week: str

    def __init__(self) -> None:
        self._min = '*'
        self._hour = '*'
        self._day = '*'
        self._month = '*'
        self._week = '*'

    def every(self, val: Union[List[int], int]) -> CronBit:
        return CronBit(self, val, 'every')

    def at(self, val: Union[List[int], int]) -> CronBit:
        return CronBit(self, val, 'at')

    @property
    def minutes(self) -> str:
        return self._min

    @minutes.setter
    def minutes(self, val: str) -> None:
        self._min = val

    @minutes.deleter
    def minutes(self) -> None:
        self._min = '*'

    @property
    def hours(self) -> str:
        return self._hour

    @hours.setter
    def hours(self, val: str) -> None:
        self._hour = val

    @hours.deleter
    def hours(self) -> None:
        self._hour = '*'

    @property
    def days(self) -> str:
        return self._day

    @days.setter
    def days(self, val: str) -> None:
        self._day = val

    @days.deleter
    def days(self) -> None:
        self._day = '*'

    @property
    def months(self) -> str:
        return self._month

    @months.setter
    def months(self, val: str) -> None:
        self._month = val

    @months.deleter
    def months(self) -> None:
        self._month = '*'

    @property
    def weekdays(self) -> str:
        return self._week

    @weekdays.setter
    def weekdays(self, val: str) -> None:
        self._week = val

    @weekdays.deleter
    def weekdays(self) -> None:
        self._week = '*'

    @property
    def is_valid(self) -> bool:
        try:
            _: croniter = self.croniter
            return True
        except CroniterBadCronError:
            return False

    def __str__(self) -> str:
        return f'{self._min} {self._hour} {self._day} {self._month} {self._week}'

    def __add__(self, other: 'CronBuilder') -> 'CronBuilder':
        out: 'CronBuilder' = CronBuilder()
        out.minutes = self.minutes
        out.hours = self.hours
        out.days = self.days
        out.months = self.months
        out.weekdays = self.weekdays
        if self.minutes == '*' and other.minutes != '*':
            out.minutes = other.minutes
        if self.hours == '*' and other.hours != '*':
            out.hours = other.hours
        if self.days == '*' and other.days != '*':
            out.days = other.days
        if self.months == '*' and other.months != '*':
            out.months = other.months
        if self.weekdays == '*' and other.weekdays != '*':
            out.weekdays = other.weekdays
        return out

    def __iadd__(self, other: 'CronBuilder') -> 'CronBuilder':
        out: 'CronBuilder' = self + other
        self.minutes = out.minutes
        self.hours = out.hours
        self.days = out.days
        self.months = out.months
        self.weekdays = out.weekdays
        return self

    @property
    def croniter(self) -> croniter:
        return croniter(str(self), datetime.now(), datetime)

    @property
    def cron(self) -> 'Cron':
        return Cron(str(self))


class Cron:
    _expr: str
    _cron: croniter

    def __init__(self, expr: str) -> None:
        self._expr = expr
        self._cron = croniter(str(self._expr), datetime.now(), datetime)

    def wrap(self, func: Callable):
        def _inner(cron: croniter, func: Callable):
            _next: datetime = cron.get_next(datetime)
            while True:
                if _next > datetime.now():
                    sleep(.5)
                    continue
                func()
                _next = cron.get_next()
        t: Thread = Thread(target=_inner, args=(self._cron, func))
        t.daemon = True
        t.start()

    @staticmethod
    def builder() -> CronBuilder:
        return CronBuilder()


def wait(func: Union[Callable, None] = None, *, until: str):
    if func is None:
        p: partial = partial(wait, until=until)
        return p

    until = until.strip()
    _patt: Pattern = compile(r'(\d+):(\d+)')
    _match: Union[Match, None] = match(_patt, until)
    if _match is None:
        raise ValueError
    int(_match.group(1))
    _h: int = int(_match.group(1))
    _m: int = int(_match.group(2))
    _until: time = time(_h, _m)

    def _inner(until_time: time, func: Callable):
        while True:
            if until_time > datetime.now().time():
                sleep(.5)
                continue
            func()
            break

    t: Thread = Thread(target=_inner, args=(_until, func))
    t.daemon = True
    t.start()
