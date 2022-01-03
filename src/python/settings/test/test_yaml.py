from pytest import raises
from ._fixtures import *


def test_yaml(fld):
    from os import chdir, remove, sep
    from ..tranquillity.settings import Yaml
    chdir(fld)
    y = Yaml()

    remove(fld + sep + 'tranquillity.yml')
    y = Yaml()
    remove(fld + sep + 'another.yml')
    y = Yaml()
    assert y.get('app.name') == 'Tranquillity'
    assert y.get('not.here', 'default') == 'default'
    with raises(Exception):
        Yaml('not_a_file.yml')
    with raises(TypeError):
        y.lookup_ns('conn.mongo.host')
    with raises(TypeError):
        y.lookup_ns({'conn.mongo.host'}, 1)

    assert y.lookup_ns([], '1') == '1'
    with raises(KeyError):
        y.lookup_ns([])
    with raises(KeyError):
        y.lookup_ns({'conn.mongo.lol'})
    assert y['conn.mongo.host'] == 'mongo'
    y['conn.mongo.host'] = 'pongo'
    assert y['conn.mongo.host'] == 'pongo'
    for _k, _v in y:
        assert isinstance(_k, str)
        assert isinstance(_v, str)
    assert y.get_eval('conn.mongo.port') == 1234
    with raises(TypeError):
        Yaml(defaults=1)
    for _k in y.keys():
        assert isinstance(_k, str)
    with raises(TypeError):
        y.get(1)
    with raises(TypeError):
        y.get('', 1)
    with raises(KeyError):
        y.get_ns('k')
    assert y.get_ns('conn.mongo.port') == '1234'
    assert isinstance(str(y), str)
    assert y.get_eval('mylist') == [1, 2, 3]
    assert y.get_bool('abool') is True
    assert y.get_bool('notabool') is True
    y._raise_on_missing = False
    with raises(KeyError):
        y.lookup_ns({'dsfsddsfd'})
    with raises(TypeError):
        y.get_bool('abool', 6)
    y = Yaml(read_only=False)
    y['val'] = 'val'
    y = Yaml(raise_on_missing=False)
    assert y['val'] == 'val'
    assert y.get_eval('val') == 'val'
    assert y.get_eval('blub') == None
    with raises(KeyError):
        y.get_ns('blub')


def test_int_float(fld):
    from os import chdir
    from ..tranquillity.settings import Yaml
    from tranquillity.exceptions import ConversionError
    chdir(fld)
    y = Yaml(raise_on_missing=False)
    assert y.get_int('blub') is None
    assert y.get_float('blub') is None
    with raises(TypeError):
        y.get_int('blub', '1')
    with raises(TypeError):
        y.lookup_int({'blub'}, '1')
    with raises(TypeError):
        y.get_float('blub', '1')
    with raises(ConversionError):
        y.get_int('conn.mongo.host')
    with raises(ConversionError):
        y.get_float('conn.mongo.host')
    with raises(KeyError):
        y.get_int_ns('blub')
    with raises(KeyError):
        y.get_float_ns('blub')
    assert y.lookup_int({'blub'}, 1) == 1
    with raises(KeyError):
        y.lookup_int_ns({'blub'})
    with raises(ValueError):
        y.lookup_int_ns({'conn.mongo.host'})
    assert y.lookup_int_ns({'conn.mongo.port'}) == 1234
    assert y.get_int_ns('conn.mongo.port') == 1234
    assert y.get_float_ns('conn.mongo.port') == 1234.


def test_internal_values(fld):
    from os import chdir
    from ..tranquillity.settings import Yaml
    chdir(fld)
    assert Yaml(read_only=1)._read_only is True
    assert Yaml(read_only=None)._read_only is False
    assert Yaml(raise_on_missing=1)._raise_on_missing is True
    assert Yaml(raise_on_missing=None)._raise_on_missing is False
    assert Yaml(defaults={'testme': {'j': '1'}}).get('testme.j') == '1'


def test_last_file(fld):
    from os import chdir, remove, sep
    from ..tranquillity.settings import Yaml
    chdir(fld)
    remove(fld + sep + 'settings.yaml')
    with raises(Exception):
        Yaml()
