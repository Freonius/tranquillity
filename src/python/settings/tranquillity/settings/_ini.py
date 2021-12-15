from .__interface import ISettings


class Ini(ISettings):
    def __init__(self) -> None:
        super().__init__()
        raise NotImplementedError
