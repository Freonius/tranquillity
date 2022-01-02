from sys import path
from os.path import realpath, dirname, sep
from datetime import date
from typing import Union, Any
from pytest import raises
path.append(realpath(dirname(__file__) +
            f'{sep}..'))


def test_dict():
    from ..tranquillity.utils import flatten_dict, unflatten_dict
    d = {'1': {'2': {'3': [1, 2, 3]}}, 'b': {'c': {}}}
    assert flatten_dict(d)[
        '1.2.3'] == str([1, 2, 3])
    assert flatten_dict({'1': {'2': {'3': [1, 2, 3]}}, 'b': {'c': {}}}, key_map=None)[
        '1.2.3'] == str([1, 2, 3])
    with raises(TypeError):
        flatten_dict({'1': 1, 2: 2})
    with raises(TypeError):
        flatten_dict({'1': 1, '2': 2}, key_prefix=2)
    with raises(TypeError):
        flatten_dict({'1': 1}, key_map=1)
    assert flatten_dict({}) == {}
    assert unflatten_dict(flatten_dict(d)) == d
    with raises(TypeError):
        unflatten_dict(1)
