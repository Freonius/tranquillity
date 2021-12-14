from .__interface import ISettings


class KVSetting(ISettings):
    def __init__(self) -> None:
        super().__init__()
        self._config({})

    def _update(self, key: str, val: str) -> None:
        pass
