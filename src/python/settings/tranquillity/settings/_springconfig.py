from .__interface import ISettings


class SpringConfig(ISettings):
    def __init__(self) -> None:
        super().__init__()
        raise NotImplementedError

    def _update(self, key: str, val: str) -> None:
        pass  # pragma: no cover
