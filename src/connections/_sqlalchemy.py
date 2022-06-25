from typing import Union, Tuple, Iterator, Type
from sqlalchemy import create_engine, Table
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.engine.url import URL
from ..exceptions import ConnectionException
from ..query._enums import SqlDialect
from .__interface import IConnection
from .__alias import T, IdType, WhereType


class Sql(IConnection):
    _client: Union[Connection, None] = None
    _dialect_enum: SqlDialect

    def _set_dialect(self, dialect: str) -> None:
        dialect = dialect.strip().lower()
        if dialect == 'mysql':
            self._dialect_enum = SqlDialect.MYSQL
        if dialect == 'sqlite':
            self._dialect_enum = SqlDialect.SQLITE
        if dialect == 'db2':
            self._dialect_enum = SqlDialect.DB2
        if dialect == 'oracle':
            self._dialect_enum = SqlDialect.ORACLE
        if dialect in ('mssql', 'sqlserver', 'sql_server'):
            self._dialect_enum = SqlDialect.MSSQL
        if dialect in ('psql', 'pgsql', 'postgre', 'postgres', 'postgresql'):
            self._dialect_enum = SqlDialect.PGSQL
        raise ConnectionException('dialect not recognised')

    def _dialect(self, dialect: str) -> str:
        dialect = dialect.strip().lower()
        if dialect == 'mysql':
            return 'mysql+mysqldb'
        if dialect == 'sqlite':
            return 'sqlite'
        if dialect == 'db2':
            return 'db2+ibm_db'
        if dialect == 'oracle':
            return 'oracle+cx_oracle'
        if dialect in ('mssql', 'sqlserver', 'sql_server'):
            return 'mssql+pymssql'
        if dialect in ('psql', 'pgsql', 'postgre', 'postgres', 'postgresql'):
            return 'postgresql+psycopg2'
        raise ConnectionException('dialect not recognised')

    def _default_port(self, dialect: str) -> Union[int, None]:
        dialect = dialect.strip().lower()
        if dialect == 'mysql':
            return 3306
        if dialect == 'sqlite':
            return None
        if dialect == 'db2':
            return 50000
        if dialect == 'oracle':
            return 1521
        if dialect in ('mssql', 'sqlserver', 'sql_server'):
            return 1433
        if dialect in ('psql', 'pgsql', 'postgre', 'postgres', 'postgresql'):
            return 5432
        raise ConnectionException('dialect not recognised')

    def connect(self) -> None:
        _dialect: Union[str, None]
        try:
            if (_dialect := self._settings.get('conn.sql.dialect')) is None:
                raise ConnectionException('dialect is not specified')
        except KeyError as e:
            raise ConnectionException('dialect is not specified') from e
        if _dialect is None:
            raise ConnectionException('dialect is not specified')
        try:
            _host: Union[str, None] = self._settings.get('conn.sql.host')
        except KeyError as e:
            if _dialect.strip().lower() == 'sqlite':
                _host = self._settings.get('conn.sql.file')
            else:
                raise ConnectionException('host is not defined') from e
        if _host is None:
            raise ConnectionException('host is not defined')
        _port: Union[int, None] = self._settings.get_int(
            'conn.sql.port', self._default_port(_dialect))

        _dialect = self._dialect(_dialect)
        _username: Union[str, None] = None
        _password: Union[str, None] = None
        try:
            _username = self._settings.get('conn.sql.user')
            _password = self._settings.get('conn.sql.password')
        except KeyError:
            pass
        _db: Union[str, None] = self._settings.get('conn.sql.db')
        _url: URL = URL(_dialect, _username, _password, _host, _port, _db)
        del _dialect, _username, _password, _host, _port
        _engine: Engine = create_engine(_url, echo=False)
        self._client = _engine.connect()

    def _is_connected(self) -> bool:
        if self._client is None:
            return False
        return not self._client.closed

    def close(self) -> None:
        if self._client is None:
            return
        self._client.close()
        self._client = None

    @property
    def client(self) -> Connection:
        if self._client is None:
            raise ConnectionException('Client is not connected')
        return self._client

    def select(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> Iterator[T]:
        return super().select(t, id, where)

    def update(self, obj: T, /, id: IdType = None, where: WhereType = None) -> Tuple[Union[T, None], bool]:
        return super().update(obj, id, where)

    def delete_where(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> int:
        return super().delete_where(t, id, where)

    def insert(self, obj: T) -> Tuple[Union[T, None], IdType, bool]:
        return super().insert(obj)

    def create_table(self, t: Type[T]) -> bool:
        _t: Table = t.alchemy_table(self.client)
        _t.create(self.client, checkfirst=True)
        return _t.exists(self.client) is True

    def drop_table(self, t: Type[T]) -> bool:
        _t: Table = t.alchemy_table(self.client)
        _t.drop(self.client, checkfirst=True)
        return _t.exists(self.client) is False

    def migrate_table(self, t: Type[T]) -> bool:
        pass
