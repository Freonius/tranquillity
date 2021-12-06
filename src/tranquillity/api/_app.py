import typing as t
from logging import Logger
from datetime import date, datetime, time
from typing import TypeVar, Union, Dict, Any, List, Tuple, Type
from flask import jsonify
from flask.wrappers import Response
from flask import Flask
from ._blueprints import ApiBlueprint
from ..data.__interface import IDBObject
from ..settings.__interface import ISettings

class App(Flask):
    _log: Logger

    def __init__(self, settings: Union[ISettings, None, str] = None, register_objects: Union[List[Dict[str, Type[IDBObject]]], None] = None):
        _name: str = ''
        super().__init__(_name,)

        @self.errorhandler(404)
        def is_404(e: Exception):
            return self.result(None)

        @self.errorhandler(401)
        def is_401(e: Exception):
            return self.result(None)

    def init_cors(self) -> None:
        pass

    def init_eureka(self) -> None:
        pass

    def init_db(self) -> None:
        pass

    @property
    def log(self) -> Logger:
        return self._log

    @staticmethod
    def generate_object(name: str, create_py_file: bool = False) -> Type[IDBObject]:
        T = TypeVar('T', str, int, float, IDBObject, list, dict, datetime, date, time)

        def _getter(self: IDBObject, key: str, t: Type[T], constraints: Union[List, None] = None) -> Union[T, None]:
            if key in self._data.keys():
                if isinstance(self._data[key], t):
                    val: T = self._data[key]
                    if isinstance(constraints, list):
                        pass
                    return val
                if self._data[key] is None:
                    return None
                raise TypeError
            return None

        t: Type[IDBObject] = type(name, (IDBObject,), {
            'name': property(lambda self: _getter(self, 'name', str))
        })

        return t

    @staticmethod
    def result(
        result: Union[Dict[str, Any],
        List[Dict[str, Any]], None],
        message: Union[str, None] = None,
        status: int = 200,
        from_cache: bool = False) -> Tuple[Response, int]:
        return jsonify({
            'result': result,
            'status': status >= 200 and status < 400,
            'message': message if message is not None else 'OK',
            'cached': from_cache,
            'date': datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
            }), status

    def create_blueprint(self, name: str, url_prefix: str, obj: Union[Type[IDBObject], None] = None) -> ApiBlueprint:
        bp: ApiBlueprint = ApiBlueprint(name, name, url_prefix=url_prefix, log=self._log)
        bp.register(self, {})
        @bp.errorhandler(404)
        def is_404(e: Exception):
            return App.result(None)

        if obj is not None:
            @bp.rule('/', method='GET', role=[''])
            def get_all():
                return self.result(None)

            @bp.rule('/', method=['POST'], role=[])
            def create_new():
                return self.result(None)

            @bp.rule('/<obj_id>', method=['GET'], role=[])
            def get_one(obj_id: Union[str, int]):
                return self.result(None)

            @bp.rule('/<obj_id>', method=['PUT'], role=[])
            def edit_one(obj_id: Union[str, int]):
                return self.result(None)

            @bp.rule('/<obj_id>', method=['DELETE'], role=[])
            def delete_one(obj_id: Union[str, int]):
                return self.result(None)

        return bp
