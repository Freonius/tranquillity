def test_env():
    from os import environ
    from ..src.settings import Env
    e = Env()
    assert isinstance(e['path'], str)
    e['xyz'] = 'xyz'
    assert e['xyz'] == 'xyz'
    assert environ['XYZ'] == 'xyz'
    assert isinstance(e.path, list)
