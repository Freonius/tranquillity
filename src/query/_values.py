from datetime import date, datetime, time
from typing import Tuple, Union


class QWhereV:
    _val: Union[None, str, date, datetime, time, int, float, object]

    def __init__(self, val: Union[None, str, date, datetime, time, int, float, object]) -> None:
        self._val = val
        pass


class QWhereVR:
    _val: Tuple[Union[None, str, date, datetime, time, int, float], ...]

    def __init__(self, min_val, max_val) -> None:
        self._val = (min_val, max_val)
        pass
