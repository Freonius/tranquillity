from .__interface import ISettings


class Api(ISettings):
    def __init__(self) -> None:
        super().__init__()
        raise NotImplementedError

    def _update(self, key: str, val: str) -> None:
        raise NotImplementedError  # pragma: no cover
