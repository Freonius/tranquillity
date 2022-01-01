from sys import path
from pytest import raises
from os.path import realpath, dirname, sep
path.append(realpath(dirname(__file__) +
            f'{sep}..'))


def test_yaml():
    from ..tranquillity.settings import Yaml
    y = Yaml()
    assert y.get('app.name') == 'Tranquillity'
    assert y.get('not.here', 'default') == 'default'
    with raises(Exception):
        Yaml('not_a_file.yml')
    with raises(ValueError):
        y.lookup_int_ns({'conn.mongo.host'})
    with raises(TypeError):
        y.lookup_ns('conn.mongo.host')
    with raises(TypeError):
        y.lookup_ns({'conn.mongo.host'}, 1)

    assert y.lookup_ns([], '1') == '1'
    with raises(KeyError):
        y.lookup_ns([])
    with raises(KeyError):
        y.lookup_ns({'conn.mongo.lol'})
    assert y.lookup_int_ns({'conn.mongo.port'}) == 1234
    assert y.get_int_ns('conn.mongo.port') == 1234
    assert y['conn.mongo.host'] == 'mongo'
    y['conn.mongo.host'] = 'pongo'
    assert y['conn.mongo.host'] == 'pongo'
    for _k, _v in y:
        assert isinstance(_k, str)
        assert isinstance(_v, str)
    assert y.get_eval('conn.mongo.port') == 1234
    assert y.get_float_ns('conn.mongo.port') == 1234.
    with raises(TypeError):
        Yaml(defaults=1)
    for _k in y.keys():
        assert isinstance(_k, str)
    assert Yaml(read_only=1)._read_only is True
    assert Yaml(read_only=None)._read_only is False
    assert Yaml(raise_on_missing=1)._raise_on_missing is True
    assert Yaml(raise_on_missing=None)._raise_on_missing is False
    assert Yaml(defaults={'testme': {'j': '1'}}).get('testme.j') == '1'
    with raises(TypeError):
        y.get(1)
    with raises(TypeError):
        y.get('', 1)
    with raises(KeyError):
        y.get_ns('k')
    assert y.get_ns('conn.mongo.port') == '1234'
    assert isinstance(str(y), str)


def test_env():
    from os import environ
    from ..tranquillity.settings import Env
    e = Env()
    assert isinstance(e['path'], str)
    e['xyz'] = 'xyz'
    assert e['xyz'] == 'xyz'
    assert environ['XYZ'] == 'xyz'
    assert isinstance(e.path, list)
