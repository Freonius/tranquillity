from pytest import raises


def test_ini(fld):
    from os import chdir
    chdir(fld)
    from ..src.settings import Ini
    i = Ini('./settings.ini')
    assert i.get('app.name') == 'Tranquillity'
    i.set('section.salutation', 'hello')
    i = Ini()
    assert i['section.salutation'] == 'hello'
    with raises(TypeError):
        Ini(1)
    with raises(Exception):
        Ini('./jjj.ini')
