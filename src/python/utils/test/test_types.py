from sys import path
from os.path import realpath, dirname, sep
from datetime import date
from typing import Union, Any
from pytest import raises
path.append(realpath(dirname(__file__) +
            f'{sep}..'))


def test_type_check():
    from ..tranquillity.utils import type_check

    @type_check
    def f(a: str, b: Union[int, float], c: Union[int, None] = None, d: Union[Any, None] = date.today(), e: Any = None) -> None:
        return None

    assert f('', 1) is None
    with raises(TypeError):
        f(1, 1, 1)

    with raises(TypeError):
        f('', '')
