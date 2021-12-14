from .__interface import ISettings


class Sqlite(ISettings):
    def __init__(self) -> None:
        super().__init__()
