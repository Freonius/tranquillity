from pytest import raises


def test_interface():
    from ..src.settings import ISettings

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
