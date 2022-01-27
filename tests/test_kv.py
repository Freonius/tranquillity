from pytest import raises


def test_kv():
    from ..src.settings import KVSetting
    k = KVSetting()
    k['a.b'] = '1'
    assert k['a.b'] == '1'
    k = KVSetting({'a': {'b': '1'}})
    assert k['a.b'] == '1'
    with raises(TypeError):
        KVSetting(1)
