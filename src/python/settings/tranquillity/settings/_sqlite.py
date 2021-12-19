from typing import Union
from .__interface import ISettings
# from sqlite3 import connect, Connection


class Sqlite(ISettings):
    # pylint: disable=too-many-arguments
    def __init__(self,
                 db_file: str,
                 table: str,
                 key_column: str,
                 value_column: str,
                 default_column: Union[str, None] = None) -> None:

        # super().__init__()
        raise NotImplementedError
    # pylint: enable=too-many-arguments

    def _update(self, key: str, val: str) -> None:
        raise NotImplementedError
