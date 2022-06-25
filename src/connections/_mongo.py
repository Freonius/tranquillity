'''
Module for Mongo operations
'''
from typing import Any, Callable, Dict, Set, Union, Iterator, Tuple, Type, List
from urllib.parse import quote_plus
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection, InsertOneResult, UpdateResult, DeleteResult
from pymongo.errors import ConnectionFailure, OperationFailure
from pymongo.database import Database
from bson import ObjectId
from bson.dbref import DBRef
from ..exceptions import ConnectionException
from .__interface import IConnection
from .__alias import T, IdType, WhereType


class Mongo(IConnection):
    '''
    Mongo connection.
    '''
    _client: Union[MongoClient, None] = None
    _db: Union[Database, None] = None

    def connect(self) -> None:
        _ks: Callable[[str], Set[str]] = lambda x: {
            x,
            f'mongo.{x}',
            f'conn.mongo.{x}'
        }
        _host: Union[str, None] = self._settings.lookup(_ks('host'))
        if _host is None:
            raise ConnectionException('host is not defined')
        _port: int = int(str(self._settings.lookup(_ks('port'), '27017')))
        _protocol: Union[str, None] = None
        try:
            _protocol = self._settings.lookup(_ks('protocol'), 'http')
        except KeyError:
            pass
        if _protocol is None:
            _protocol = 'http'
        _username: Union[str, None] = None
        _password: Union[str, None] = None
        try:
            _username = self._settings.lookup(_ks('user'))
            _password = self._settings.lookup(_ks('password'))
        except KeyError:
            pass
        _url: str = 'mongodb://'
        if not (_username is None or _username.strip() == '' or _password is None or _password.strip() == ''):
            _url += f'{quote_plus(_username)}:{quote_plus(_password)}@'
        _url += _host
        try:

            self._client = MongoClient(host=_url, port=_port,)
            self._log_debug(f'Connected to MongoDb {_host}:{_port}')
        except ConnectionFailure:
            self._client = None
        del _username, _password, _host, _port, _protocol, _url
        if self._client is None:
            raise ConnectionException('Could not connect to MongoDB')
        _db_name: str = self._settings.lookup_ns(_ks('db'))
        del _ks
        _db: Union[Database, None] = None
        try:
            _db = self._client.get_database(_db_name)
        except Exception:
            _db = None
        self._db = _db

    def close(self) -> None:
        if self._client is None:
            return
        if self._is_connected() is False:
            self._client = None
            return
        self._client.close()

    def _is_connected(self) -> bool:
        if self._client is None:
            return False
        try:
            self._client.admin.command('ismaster')
            return True
        except ConnectionFailure:
            return False

    @property
    def client(self) -> MongoClient:
        if self._client is None:
            raise ConnectionError
        return self._client

    @property
    def db(self) -> Database:
        if self._db is None:
            raise ConnectionException
        return self._db

    def select(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> Iterator[T]:
        _query: Dict[str, Any] = {}
        if id is not None and isinstance(id, (ObjectId, str)):
            if isinstance(id, str):
                id = ObjectId(id)
            _query['_id'] = id
        _coll: Collection = self.db.get_collection(t.get_table())
        for _doc in _coll.find(_query):
            if isinstance(_doc, dict):
                yield t(**_doc)

    def delete_where(self, t: Type[T], /, id: IdType = None, where: WhereType = None) -> int:
        _query: Dict[str, Any] = {}
        if id is not None and isinstance(id, (ObjectId, str)):
            if isinstance(id, str):
                id = ObjectId(id)
            _query['_id'] = id
        _coll: Collection = self.db.get_collection(t.get_table())
        _res: DeleteResult = _coll.delete_many(_query)
        _out: int = 0
        if isinstance(_res.deleted_count, int):
            _out = _res.deleted_count
        return _out

    def insert(self, obj: T) -> Tuple[Union[T, None], IdType, bool]:
        _coll: Collection = self.db.get_collection(obj.get_table())
        _res: InsertOneResult = _coll.insert_one(obj.serialize())
        _success: bool = _res.acknowledged
        _id: Union[ObjectId, None, List] = _res.inserted_id
        if isinstance(_id, list) and len(_id) == 1 and all([isinstance(x, ObjectId) for x in _id]):
            _id = _id[0]
        if not isinstance(_id, ObjectId):
            _id = None
        obj.set_id(_id)
        return obj, _id, _success

    def update(self, obj: T, /, id: IdType = None, where: WhereType = None) -> Tuple[Union[T, None], bool]:
        _query: Dict[str, Any] = {}
        if id is None and obj.get_id() is not None:
            id = obj.get_id()
        if id is not None and isinstance(id, (ObjectId, str)):
            if isinstance(id, str):
                id = ObjectId(id)
            _query['_id'] = id
        _coll: Collection = self.db.get_collection(obj.get_table())
        _res: UpdateResult = _coll.update_one(_query, obj.serialize())
        _success: bool = _res.acknowledged and _res.modified_count == 1
        return obj, _success

    def create_table(self, t: Type[T]) -> bool:
        _id_field: Union[str, None] = t.get_id_field()
        _index: Dict[str, int] = {}
        for _fld, _dty in t.get_fields():
            if _fld == _id_field:
                continue
            if _dty.is_primary_key:
                _index[_fld] = ASCENDING
        if len(_index.keys()) == 0:
            return True
        _coll: Collection = self.db.get_collection(t.get_table())
        _index_name: str = f'{t.__name__.lower()}_index'
        _res: List[str] = _coll.create_index(
            _index, unique=True, name=_index_name)
        return _index_name in _res

    def drop_table(self, t: Type[T]) -> bool:
        try:
            _coll: Collection = self.db.get_collection(t.get_table())
            _index_name: str = f'{t.__name__.lower()}_index'
            _coll.drop_index(_index_name)
            return True
        except (OperationFailure, TypeError):
            return False
