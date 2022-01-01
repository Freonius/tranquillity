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
