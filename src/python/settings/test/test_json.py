from pytest import raises
from ._fixtures import *


def test_json(fld):
    from os import chdir, remove, sep
    chdir(fld)
    from ..tranquillity.settings import Json
    from tranquillity.exceptions import NotAllowedOperation
    j = Json()
    assert j['value.value'] == '2'
    j['value.value'] = '3'
    assert j['value.value'] == '3'
    with raises(TypeError):
        j.set(1, 1)
    with raises(TypeError):
        j.set('1', 1)
    j = Json(read_only=True)
    with raises(NotAllowedOperation):
        j.set('val', 'val')
    j = Json(read_only=False)
    j.set('val', 'val')
    j = Json()
    assert j['val'] == 'val'
    remove(fld + sep + 'settings.json')
    with raises(Exception):
        j = Json()
