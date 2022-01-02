from sys import path
from pytest import raises
from os.path import realpath, dirname, sep
from pytest import fixture
from _pytest.tmpdir import TempdirFactory

path.append(realpath(dirname(__file__) +
            f'{sep}..'))


@fixture(scope='session')
def fld(tmpdir_factory: TempdirFactory):
    fld = tmpdir_factory.mktemp('test')
    fn = fld.join('tranquillity.yml')
    JSON = '''
    { "value": { "value": 2 } }
    '''
    YAML = '''
app:
  name: Tranquillity
conn:
  mongo:
    host: mongo
    port: 1234
mylist:
  - 1
  - 2
  - 3
abool: true
notabool: 1
'''
    with open(fn, 'w') as fh:
        fh.write(YAML)
    with open(fld.join('settings.yaml'), 'w') as fh:
        fh.write(YAML)
    with open(fld.join('settings.json'), 'w') as fh:
        fh.write(JSON)
    with open(fld.join('another.yml'), 'w') as fh:
        fh.write('')
    return str(fld)


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
    assert y.get_eval('mylist') == [1, 2, 3]
    assert y.get_bool('abool') is True
    assert y.get_bool('notabool') is True
    y._raise_on_missing = False
    with raises(KeyError):
        y.lookup_ns({'dsfsddsfd'})
    with raises(TypeError):
        y.get_bool('abool', 6)


def test_env():
    from os import environ
    from ..tranquillity.settings import Env
    e = Env()
    assert isinstance(e['path'], str)
    e['xyz'] = 'xyz'
    assert e['xyz'] == 'xyz'
    assert environ['XYZ'] == 'xyz'
    assert isinstance(e.path, list)


def test_json(fld):
    from os import chdir, remove, sep
    chdir(fld)
    from ..tranquillity.settings import Json
    j = Json()
    assert j['value.value'] == '2'
    j['value.value'] = '3'
    assert j['value.value'] == '3'
    remove(fld + sep + 'settings.json')
    with raises(Exception):
        j = Json()


def test_interface():
    from ..tranquillity.settings import ISettings

    class T(ISettings):
        def __init__(self) -> None:
            super().__init__()
            self._config(1)

        def _update(self, key: str, val: str) -> None:
            return super()._update(key, val)

    class T2(ISettings):
        def __init__(self) -> None:
            super().__init__()
            self._config({'key': 'val'}, required_fields=['key2'])

        def _update(self, key: str, val: str) -> None:
            return super()._update(key, val)

    class T3(ISettings):
        def __init__(self) -> None:
            super().__init__()
            self._config({'key': 'val'}, raise_on_missing=False,
                         defaults={'yep': '1'})

        def _update(self, key: str, val: str) -> None:
            return super()._update(key, val)

    with raises(TypeError):
        T()

    with raises(KeyError):
        T2()

    t = T3()
    assert t.get('nope') is None
    assert t.get('yep') == '1'
    with raises(KeyError):
        t._raise_on_missing = True
        t.get('nope')
