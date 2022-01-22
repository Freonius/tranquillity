from typing import Union, Dict
from sqlite3 import connect, Connection, Cursor, ProgrammingError
from .__interface import ISettings


class Sqlite(ISettings):
    _connection: Connection
    _key_col: str
    _val_col: str
    _tbl: str
    _db_file: str

    # pylint: disable=too-many-arguments
    def __init__(self,
                 db_file: Union[str, None] = None,
                 table: Union[str, None] = None,
                 key_column: Union[str, None] = None,
                 value_column: Union[str, None] = None,
                 default_column: Union[str, None] = None,
                 raise_on_missing: bool = True,
                 read_only: bool = False) -> None:

        super().__init__()
        _vals: Dict[str, str] = Sqlite.create_stmt_if_not_exists(
            db_file, table, key_column, value_column, default_column)
        self._db_file = _vals['db_file']
        self._connection = connect(self._db_file)
        self._connection.execute(_vals['create_statement'])
        self._key_col = _vals['key_column']
        self._val_col = _vals['value_column']
        self._tbl = _vals['table']
        _curs: Cursor = self._connection.execute(
            f'SELECT {self._key_col}, {self._val_col} FROM {self._tbl};')
        _d: Dict[str, str] = {str(x[0]): str(x[1]) for x in _curs.fetchall()}
        self._config(_d, raise_on_missing=raise_on_missing,
                     read_only=read_only)

    @staticmethod
    def create_stmt_if_not_exists(db_file: Union[str, None] = None,
                                  table: Union[str, None] = None,
                                  key_column: Union[str, None] = None,
                                  value_column: Union[str, None] = None,
                                  default_column: Union[str, None] = None) -> Dict[str, str]:
        if db_file is None:
            db_file = './settings.db:cachedb?mode=memory&cache=shared'
        if table is None:
            table = 'settings'
        if key_column is None:
            key_column = 'key_column'
        if value_column is None:
            value_column = 'value_column'
        if default_column is None:
            default_column = 'default_column'
        _stmt: str = f'''
            CREATE TABLE IF NOT EXISTS {table} 
            (
                {key_column} TEXT PRIMARY KEY NOT NULL,
                {value_column} TEXT NOT NULL,
                {default_column} TEXT
            );
'''
        return {
            'db_file': db_file,
            'table': table,
            'key_column': key_column,
            'value_column': value_column,
            'default_column': default_column,
            'create_statement': _stmt
        }

    # pylint: enable=too-many-arguments

    def close(self) -> None:
        self._connection.close()

    def connect(self) -> None:
        self._connection = connect(self._db_file)

    @property
    def is_connected(self) -> bool:
        try:
            self._connection.cursor()
            return True
        except ProgrammingError:
            return False

    def _update(self, key: str, val: str) -> None:
        _f: str = f'''INSERT INTO {self._tbl} ({self._key_col}, {self._val_col})
                          VALUES(?, ?)
                      ON CONFLICT ({self._key_col}) DO UPDATE SET
                          {self._val_col}=?;'''
        self._connection.execute(_f, (key, val, val))
        self._connection.commit()
