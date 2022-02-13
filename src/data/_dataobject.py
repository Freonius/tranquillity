from abc import ABC
from types import NotImplementedType
from typing import Any, Callable, Dict, List, Tuple, Union, Iterator, Iterable, TypeVar, Type, TYPE_CHECKING
from inspect import getmembers
from json import loads, dumps
from copy import deepcopy
from datetime import date, datetime
from io import StringIO
from string import Template
from rule_engine import type_resolver_from_dict, Context, DataType, Rule
from graphene import ObjectType
from sqlalchemy import Table
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.schema import MetaData
from pandas import Series, DataFrame
from numpy import dtype
from tornado.web import RequestHandler
from tornado.escape import json_decode
from bson import ObjectId
from .types._dtype import DType
from .types._id import Id, MongoId
from ..utils._classproperty import classproperty
from ..exceptions import ValidationError, ConnectionException
from ..settings.__interface import ISettings

if TYPE_CHECKING is True:
    from ..connections.__interface import IConnection

T = TypeVar('T', bound='DataObject')


class DataObject(ABC):
    __table__: str = NotImplemented
    __schema__: Union[str, None] = None
    __db__: Union[str, None] = None
    __data__: Dict[str, DType]
    __cache__: Union['IConnection', None, Type['IConnection']] = None
    __conn__: Union['IConnection', None, Type['IConnection']] = None
    __urlprefix__: str = r'/api/v1/'
    __settings__: Union[ISettings, None] = None

    def __init__(self: T, **data) -> None:
        # TODO: Get things from isettings
        self.__data__ = {}
        for dkey, dtype in self.get_fields():
            self.__data__[dkey] = deepcopy(dtype)
        for key, val in data.items():
            self[key] = val
        # self.validate()

    @classmethod
    def get_table(cls: Type[T]) -> str:
        _t: str
        if cls.__table__ is None or isinstance(cls.__table__, NotImplementedType):
            _t = cls.__name__
        else:
            _t = cls.__table__
        if cls.__schema__ is None:
            return _t
        return cls.__schema__ + '.' + _t

    @classmethod
    def to_graphql(cls) -> Type[ObjectType]:
        flds = cls.get_fields()
        return type('GQL' + cls.__class__.__name__, (ObjectType,), {
            x[0]: x[1].get_graphql_type() for x in flds
        })

    @classmethod
    def alchemy_table(cls, engine: Union[Engine, Connection, None] = None) -> Table:
        cols = [x.get_sqlalchemy_column() for _, x in cls.get_fields()]
        metadata = MetaData(bind=engine)
        tbl: str = ''
        if isinstance(cls.__table__, NotImplementedType):
            tbl = cls.__name__.lower()
        else:
            tbl = cls.__table__
        t = Table(tbl, metadata, schema=cls.__schema__)
        for col in cols:
            t.append_column(col)
        return t

    def get_graphql_type(self) -> ObjectType:
        attr = {
            x[0]: x[1].get_graphql_type() for x in self.__data__.items()
        }

        def _look(s, k):
            try:
                return s.__data__[k].value
            except:
                for _, f in s.__data__.items():
                    if f.fiels == k:
                        return f.value
        attr['__data__'] = deepcopy(self.__data__)
        attr['__getitem__'] = lambda s, k: _look(s, k)
        for x, _ in self.__data__.items():
            attr['resolve_' + x] = lambda s, *a, **k: s[x]
        # attr['resolve_filter'] = lambda s, *a, **k: 'I am a filter'
        return type('GQL' + self.__class__.__name__, (ObjectType,), attr)

    def serialize(self) -> Dict[str, Any]:
        return self.to_dict()

    @classmethod
    def _get_rule_engine_context(cls: Type[T]) -> Context:
        _ctx: Dict[str, Any] = {}
        for _, fld in cls.get_fields():
            _t_ctx: Union[None, Any] = None
            try:
                _t_ctx = DataType.from_type(fld.get_type())
            except ValueError:
                if fld.is_dict:
                    _t_ctx = DataType.MAPPING(
                        DataType.STRING, DataType.UNDEFINED, fld.is_nullable)
                else:
                    _t_ctx = DataType.UNDEFINED
            if fld.is_list:
                _t_ctx = DataType.ARRAY(_t_ctx, fld.is_nullable)
            if _t_ctx is None:
                _t_ctx = DataType.UNDEFINED
            _ctx[fld.field] = _t_ctx
        return Context(type_resolver=type_resolver_from_dict(_ctx))

    @classmethod
    def _filter_re_rule(cls: Type[T], objects: Iterable[T], rule: str) -> List[T]:
        out: List[T] = []
        re_rule: Rule = Rule(rule, context=cls._get_rule_engine_context())
        for o in objects:
            if isinstance(o, cls) and re_rule.matches(o.to_dict()):
                out.append(o)
        return out

    @classmethod
    def filter(cls: Type[T], objects: Iterable[T], rule: Union[Callable[[T], bool], str]) -> List[T]:
        if isinstance(rule, str):
            return cls._filter_re_rule(objects, rule)
        out: List[T] = []
        for obj in objects:
            if isinstance(obj, cls) and rule(obj):
                out.append(obj)
        return out

    def validate(self) -> None:
        for _, fld in self.__data__.items():
            fld.validate()

    @property
    def is_valid(self) -> bool:
        try:
            self.validate()
            return True
        except ValidationError:
            return False

    def to_json(self) -> str:
        out: Dict[str, Any] = {}
        for _, fld in self.__data__.items():
            out[fld.json_field] = fld.serialize()
        return dumps(out, indent=None)

    @classmethod
    def from_json(cls: Type[T], body: str) -> T:
        return cls(**loads(body))

    @classmethod
    def from_pickle(cls: Type[T], body: bytes) -> T:
        pass  # TODO

    @classmethod
    def from_df(cls: Type[T], df: DataFrame) -> List[T]:
        out: List[T] = []
        for _, d in df.iterrows():
            out.append(cls(**d))
        return out

    @classmethod
    def get_fields(cls) -> Iterator[Tuple[str, DType]]:
        for _fld_name, _fld_val in getmembers(cls):
            if isinstance(_fld_val, DType):
                if not isinstance(_fld_val.field, str):
                    _fld_val.field = _fld_name
                yield _fld_name, _fld_val

    def __getitem__(self, key: str) -> Any:
        for _fld_name, _fld_val in self.__data__.items():
            if key in (_fld_name, _fld_val.field, _fld_val.json_field):
                return _fld_val.value
        raise KeyError(f'Key {key} not found')

    def __setitem__(self, key: str, val: Any) -> None:
        for _fld_name, _fld_val in self.__data__.items():
            if key in (_fld_name, _fld_val.field, _fld_val.json_field):
                _fld_val.value = val
                return
        raise KeyError(f'Key {key} not found')

    def get(self, key: str) -> Any:
        return self[key]

    def set(self, key: str, val: Any) -> None:
        self[key] = val

    @classmethod
    def create_table(cls) -> bool:
        raise NotImplementedError

    def add_to_db(self, mode: str = 'upsert') -> bool:
        if self.__conn__ is None:
            raise Exception
        _conn: 'IConnection'
        if isinstance(self.__conn__, type):
            _conn = self.__conn__(self.__settings__)
        else:
            _conn = self.__conn__
        with _conn:
            raise NotImplementedError

    def add_to_cache(self) -> bool:
        raise NotImplementedError

    def get_id(self) -> Union[int, ObjectId, str, None]:
        for _, dty in self.get_fields():
            if isinstance(dty, (Id, MongoId)):
                return dty.value
        return None

    def set_id(self, id: Union[int, ObjectId, str, None]) -> None:
        for _, dty in self.get_fields():
            if isinstance(dty, (Id, MongoId)):
                dty.value = id
                return

    @classmethod
    def get_from_db(cls: Type[T], id: Union[int, str, None] = None, where_conditions: Union[Iterable[str], None] = None) -> List[T]:
        raise NotImplementedError

    @classmethod
    def get_from_cache(cls: Type[T], id: Union[int, str, None] = None, where_conditions: Union[Iterable[str], None] = None) -> List[T]:
        raise NotImplementedError

    def delete_from_db(self) -> bool:
        raise NotImplementedError

    def delete_from_cache(self) -> bool:
        raise NotImplementedError

    def keys(self) -> Iterator[str]:
        for fld, _ in self:
            yield fld

    def items(self) -> Iterator[Tuple[str, Any]]:
        for fld, val in self:
            yield fld, val

    def to_dict(self) -> Dict[str, Any]:
        _out: Dict[str, Any] = {}
        for _k, _v in self:
            _out[_k] = _v
        return _out

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for _, fld in self.__data__.items():
            yield fld.field, deepcopy(fld.iter_value())

    def __repr__(self) -> str:
        _id: str = ' '.join(list([x[1].field + '=' + str(x[1])
                            for x in self.__data__.items() if x[1].is_id]))
        _id = _id.strip()
        _sp: str = ' ' if len(_id) > 0 else ''
        return f'<{self.__class__.__name__}{_sp}{_id}>'

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, type(self)):
            return False
        for a, _ in self:
            if self[a] != __o[a]:
                return False
        return True

    def __ne__(self, __o: object) -> bool:
        if self == __o:
            return False
        return True

    @classmethod
    def to_es_mapping(cls) -> Dict[str, Dict[str, Dict[str, Dict[str, str]]]]:
        def _to_es_type(x: DType) -> Dict[str, str]:
            return {'type': 'keyword'}    # TODO
        return {'mappings': {'properties': {x.field: _to_es_type(x) for _, x in cls.get_fields()}}}

    @classmethod
    def to_df(cls: Type[T], objects: Iterable[T]) -> DataFrame:
        _dtypes: List[Tuple[str, Series]] = []
        _conv: List[Dict[str, Any]] = list([y.to_dict() for y in objects])
        for _, x in cls.get_fields():
            _t: Type = x.get_type()
            if _t is int:
                _dtypes.append((x.field,
                                Series(data=[c[x.field] for c in _conv], name=x.field, dtype='Int64')))
            elif _t is float:
                _dtypes.append((x.field,
                                Series(data=[c[x.field] for c in _conv], name=x.field, dtype=dtype('float64'))))
            elif _t is datetime:
                _dtypes.append((x.field, Series(data=[c[x.field] for c in _conv], name=x.field,
                               dtype=dtype('datetime64[ns]'))))
            elif _t is date:
                _dtypes.append((x.field,
                                Series(data=[c[x.field] for c in _conv], name=x.field, dtype=dtype('datetime64[D]'))))
            else:
                _dtypes.append((x.field,
                                Series(data=[c[x.field] for c in _conv], name=x.field, dtype=dtype(_t))))
        df: DataFrame = DataFrame(data={k: v for k, v in _dtypes})
        return df

    @classmethod
    def to_ts(cls) -> str:
        # TODO: Complete types and write from json method
        string: StringIO = StringIO()
        string.write('class ' + cls.__name__ + ' {\n')
        _t: Template = Template('  $field: $type\n')
        for _, x in cls.get_fields():
            _fld_type: str
            if x.get_type() in (int, float):
                _fld_type = 'number'
            elif x.get_type() is str:
                _fld_type = 'string'
            else:
                _fld_type = 'any'
            string.write(_t.substitute({'field': x.field, 'type': _fld_type}))
        string.write('}')
        return string.getvalue()

    @classmethod
    def to_dart(cls) -> str:
        pass  # TODO

    @classmethod
    def to_python(cls: Type[T]) -> str:
        raise NotImplementedError

    @classmethod
    def to_api(cls: Type[T]) -> Tuple[str, Type[RequestHandler]]:
        class DataRequest(RequestHandler):
            __object__: Type[T] = cls

            def write_error(self, status_code: int, **kwargs: Any) -> None:
                self.add_header('Content-Type', 'application/json')
                _msg: str = self._reason
                if 'exc_info' in kwargs:
                    if isinstance(kwargs['exc_info'], tuple):
                        for x in kwargs['exc_info']:
                            if isinstance(x, Exception):
                                _msg = str(x)
                self.write({'result': None, 'success': False, 'status_code': status_code,
                            'message': _msg, 'datetime': datetime.now().isoformat()})
                self.set_status(500)

            def get(self, id: Union[int, str, None]):
                self.add_header('Content-Type', 'application/json')
                if isinstance(id, str) and len(id.strip()) == 0:
                    id = None
                if self.__object__.__conn__ is None:
                    raise ConnectionException('No db connection')
                conditions = []

                for fld, dty in self.__object__.get_fields():
                    if id is not None and isinstance(dty, (Id, MongoId)):
                        conditions.append(
                            eval(f'self.__object__.{fld}') == id)
                        continue
                    if fld in self.request.arguments.keys():
                        conditions.append(
                            eval(f'self.__object__.{fld}') == self.get_argument(fld))
                        continue
                if self.__object__.__conn__ is None:
                    self.write({'result': [x(1) for x in conditions], 'success': True, 'status_code': 200,
                               'message': 'OK', 'datetime': datetime.now().isoformat()})
                    self.set_status(200)
                    return
                # TODO: Actual return

            def post(self, id: Union[int, str, None] = None):
                _data = json_decode(self.request.body)
                _obj: T = self.__object__(**_data)
                self.write({'result': _obj.to_dict(), 'success': True, 'status_code': 200,
                            'msg': 'OK', 'datetime': datetime.now().isoformat()})
                self.set_status(200)

        return (cls.__urlprefix__ + cls.__name__.lower() + r'/?([^/]+)?/?', DataRequest)
