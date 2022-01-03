from pytest import raises
from ._fixtures import *


def test_ini(fld):
    from os import chdir
    chdir(fld)
    from ..tranquillity.settings import Ini
    i = Ini('./settings.ini')
    assert i.get('app.name') == 'Tranquillity'
    i.set('section.salutation', 'hello')
    i = Ini()
    assert i['section.salutation'] == 'hello'
    with raises(TypeError):
        Ini(1)
    with raises(Exception):
        Ini('./jjj.ini')
