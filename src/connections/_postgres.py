
from typing import Any, Callable, List, Union, Dict, Tuple, Iterator, Type, TYPE_CHECKING
from datetime import date, time, datetime
from psycopg2 import connect, cursor
from psycopg2._psycopg import connection
from psycopg2.sql import SQL, Identifier
from ..exceptions import ConnectionException
from ..query._where import _id2wc, _wc2psql
from .__interface import IConnection
from .__alias import T, WhereType, IdType, WhereCondition
from .__dataclasses import PgColumn

if TYPE_CHECKING is True:
    from ..data.types._dtype import DType


class Postgres(IConnection):
    _client: Union[connection, None] = None

    @property
    def client(self) -> connection:
        if self._client is None:
            raise ConnectionException('Connection is not set')
        return self._client

    def _is_connected(self) -> bool:
        if self._client is None:
            return False
        _status: int = self._client.status
        return _status > 0

    def connect(self) -> None:
        _port: Union[int, None] = None
        try:
            if (_port := self._settings.get_int('conn.postgres.port')) is None:
                _port = 5432
        except KeyError:
            _port = 5432

        _user: Union[str, None] = None
        _pwd: Union[str, None] = None

        try:
            _user = self._settings.get('conn.postgres.user')
        except KeyError:
            pass

        try:
            _pwd = self._settings.get('conn.postgres.password')
        except KeyError:
            pass

        _data: Dict[str, Union[str, int, None]] = {
            'host': self._settings.get_ns('conn.postgres.host'),
            'port': _port,
            'database': self._settings.get_ns('conn.postgres.db'),
            'user': _user,
            'password': _pwd,
        }
        self._client = connect(**_data)

    def close(self) -> None:
        if self._client is None:
            return
        self._client.close()
        self._client = None

    def _get_table_from_obj(self, t: Union[Type[T], T]) -> SQL:
        if t.__schema__ is None:
            return SQL('public.{0}').format(Identifier(t.get_table()))
        _s, _t = t.get_table().split('.')
        return SQL('{0}.{1}').format(
            Identifier(_s),
            Identifier(_t),
        )

    def insert(self, obj: T) -> Tuple[Union[T, None], IdType, bool]:
        _dict: Dict[str, Any] = obj.to_dict()
        _id_field: Union[str, None] = obj.get_id_field()
        if _id_field is not None and _id_field in _dict.keys():
            del _dict[_id_field]
        _query: SQL = SQL('INSERT INTO {0} ({1}) VALUES ({2}) RETURNING {3}').format(
            self._get_table_from_obj(obj),
            SQL(', ').join([Identifier(x) for x in _dict.keys()]),
            SQL(', '.join(['%s' for _ in range(len(_dict.keys()))])),
            Identifier(_id_field)
        )
        _crs: cursor = self.client.cursor()
        _crs.execute(_query, vars=tuple(_dict.values()))
        self.client.commit()
        _success: bool = _crs.rowcount == 1
        _id: IdType = None
        try:
            _id = _crs.fetchone()[0]
        except Exception:
            pass
        if _id is not None:
            obj.set_id(_id)
        return obj, _id, _success

    def update(self, obj: T, /, id: IdType = None, where: WhereType = None) -> Tuple[Union[T, None], bool]:
        _vars: List[Any] = []
        _data: Dict[str, Any] = obj.to_dict()
        for _x in _data.values():
            _vars.append(_x)

        if where is None:
            where = []
        _id_field: Union[str, None] = obj.get_id_field()
        if id is not None and _id_field is not None:
            where.append(_id2wc(_id_field, id))
        _lwc: List[Tuple[WhereCondition, bool,
                         Tuple[Union[None, str, date, datetime,
                                     time, int, float, object], ...]]] = list([_wc2psql(x) for x in where])

        for _l in _lwc:
            if _l[1] is True:
                for _v in _l[2]:
                    _vars.append(_v)

        _query: SQL = SQL('UPDATE {0} SET {1}{2}{3}').format(
            self._get_table_from_obj(obj),
            SQL(', ').join([SQL('{0} = %s').format(
                Identifier(x) for x in _data.keys())]),
            SQL('') if len(where) == 0 else SQL(' WHERE '),
            SQL(' AND ').join([x[0] for x in _lwc])
        )
        _crs: cursor = self.client.cursor()
        _crs.execute(_query, vars=tuple(_vars))
        self.client.commit()
        return obj, _crs.rowcount == 1

    def select(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> Iterator[T]:
        _fields: List[Identifier] = []
        _fields_str: List[str] = list([fld for fld, _ in t.get_fields()])
        _fields_str.sort()
        _fields = list([Identifier(x) for x in _fields_str])
        if where is None:
            where = []
        _id_field: Union[str, None] = t.get_id_field()
        if id is not None and _id_field is not None:
            where.append(_id2wc(_id_field, id))
        _lwc: List[Tuple[WhereCondition, bool,
                         Tuple[Union[None, str, date, datetime,
                                     time, int, float, object], ...]]] = list([_wc2psql(x) for x in where])
        _vars: List[Union[None, str, date, datetime,
                          time, int, float, object]] = []
        for _l in _lwc:
            if _l[1] is True:
                for _v in _l[2]:
                    _vars.append(_v)

        _query: SQL = SQL('SELECT {0} FROM {1}{2}{3}').format(
            SQL(', ').join(_fields),
            self._get_table_from_obj(t),
            SQL('') if len(where) == 0 else SQL(' WHERE '),
            SQL(' AND ').join([x[0] for x in _lwc])
        )
        _crs: cursor = self.client.cursor()
        _crs.execute(_query, vars=tuple(_vars))
        for _res in _crs.fetchall():
            if len(_fields_str) == len(_res):
                _data = {}
                for _name, _value in zip(_fields_str, _res):
                    _data[_name] = _value
                yield t(**_data)
        _crs.close()

    def delete_where(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> int:
        if where is None:
            where = []
        _id_field: Union[str, None] = t.get_id_field()
        if id is not None and _id_field is not None:
            where.append(_id2wc(_id_field, id))
        _lwc: List[Tuple[WhereCondition, bool,
                         Tuple[Union[None, str, date, datetime,
                                     time, int, float, object], ...]]] = list([_wc2psql(x) for x in where])
        _vars: List[Union[None, str, date, datetime,
                          time, int, float, object]] = []
        for _l in _lwc:
            if _l[1] is True:
                for _v in _l[2]:
                    _vars.append(_v)

        _query: SQL = SQL('DELETE FROM {0}{1}{2}').format(
            self._get_table_from_obj(t),
            SQL('') if len(where) == 0 else SQL(' WHERE '),
            SQL(' AND ').join([x[0] for x in _lwc])
        )
        _crs: cursor = self.client.cursor()
        _crs.execute(_query, vars=tuple(_vars))
        self.client.commit()
        return int(_crs.rowcount)

    def create_table(self, t: Type[T]) -> bool:
        _schema: str = t.__schema__ if t.__schema__ is not None else 'public'
        _tbl: SQL = self._get_table_from_obj(t)
        _queries: List[SQL] = []
        if self.table_exists(t.__table__, _schema):
            # Table exists, edit
            _definition: List[PgColumn] = self.describe_table(
                t.__table__, _schema)
            _cols: List[str] = []
            _dtype: 'DType'
            for _, _dtype in t.get_fields():
                _col: str = _dtype.field.lower().strip()
                _cols.append(_col)
                _found: List[PgColumn] = list(
                    filter(lambda x: _col == x.column_name.lower().strip(), _definition))
                _found_col: Union[PgColumn, None] = None
                if len(_found) == 1:
                    _found_col = _found[0]
                del _found
                if _found_col is None:
                    pass  # TODO: add column
                else:
                    pass  # TODO: check if it's the same
            _cols_to_drop: List[PgColumn] = list(
                filter(lambda x: x.column_name.lower().strip() not in _cols, _definition))
            for _col_to_drop in _cols_to_drop:
                _queries.append(SQL('ALTER TABLE {0} DROP COLUMN {1} CASCADE').format(
                    _tbl,
                    Identifier(_col_to_drop.column_name)
                ))
        else:
            pass  # TODO: Create table
        if len(_queries) == 0:
            return True
        _crs: cursor = self.client.cursor()
        try:
            for _query in _queries:
                _crs.execute(_query)
            self.client.commit()
            _crs.close()
            return True
        except Exception:
            return False

    def drop_table(self, t: Type[T], cascade: bool = True) -> bool:
        _query: SQL = SQL('DROP TABLE IF EXISTS {0}{1}').format(
            self._get_table_from_obj(t),
            SQL(' CASCADE') if cascade is True else SQL('')
        )
        _crs: cursor = self.client.cursor()
        _crs.execute(_query)
        self.client.commit()
        _crs.close()
        return True

    def describe_table(self, table: str, schema: str = 'public') -> List[PgColumn]:
        _query: SQL = SQL('''SELECT
                                column_name AS name,
                                column_default AS default,
                                CASE is_nullable WHEN 'YES' THEN TRUE ELSE FALSE END AS is_nullable,
                                udt_name AS type,
                                CASE is_identity WHEN 'YES' THEN TRUE ELSE FALSE END AS is_identity
                            FROM
                            information_schema.columns
                            WHERE table_name = %s AND table_schema = %s;''')
        _crs: cursor = self.client.cursor()
        _crs.execute(_query, vars=(table, schema))
        _out: List[PgColumn] = []
        for _res in _crs.fetchall():
            if not isinstance(_res, tuple) or len(_res) != 5:
                continue
            _name: Any = _res[0]
            _default: Any = _res[1]
            _is_nullable: Any = _res[2]
            _type: Any = _res[3]
            _is_identity: Any = _res[4]
            if not isinstance(_name, str) or not isinstance(_type, str):
                continue
            if not isinstance(_is_identity, bool) or not isinstance(_is_nullable, bool):
                continue
            _out.append(PgColumn(_name, _default, _type,
                        _is_nullable, _is_identity))
        return _out

    def table_exists(self, table: str, schema: str = 'public') -> bool:
        _query: SQL = SQL('''SELECT
                                CASE COUNT(*) WHEN 1 THEN TRUE ELSE FALSE END AS exists
                            FROM information_schema.tables
                            WHERE table_name = %s AND table_schema = %s;''')
        _crs: cursor = self.client.cursor()
        _crs.execute(_query, vars=(table, schema))
        _res = _crs.fetchone()
        _exists: bool = False
        if isinstance(_res, tuple) and len(_res) > 0 and isinstance(_res[0], bool):
            _exists = _res[0]
        return _exists
