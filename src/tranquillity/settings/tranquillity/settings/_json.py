from .__interface import ISettings


class Json(ISettings):
    def __init__(self, json_file: str) -> None:
        super().__init__()
