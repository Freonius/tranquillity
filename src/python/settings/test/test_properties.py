from pytest import raises
from ._fixtures import *


def test_properties(fld):
    from os import chdir
    chdir(fld)
    from ..tranquillity.settings import Properties
    i = Properties('./settings.properties')
    assert i.get('app.name') == 'Tranquillity'
    i['section.abc'] = 'abc'
    i = Properties('./settings.properties')
    assert i['section.abc'] == 'abc'
    with raises(TypeError):
        Properties(1)
    with raises(Exception):
        Properties('./jjj.ini')
