from logging import Logger
from datetime import date, datetime, time
from typing import TypeVar, Union, Dict, Any, List, Tuple, Type
from flask import jsonify
from flask.wrappers import Response
from flask import Flask
from ._blueprints import ApiBlueprint
from tranquillity.settings import Yaml, ISettings


class App(Flask):
    _log: Logger
    _port: int

    def __init__(self, settings: Union[ISettings, None, str] = None):
        if settings is None:
            settings = Yaml()
        if isinstance(settings, str):
            settings = Yaml(settings)
        _name: str = settings.get_ns('app.name')
        self._port = settings.get_int_ns('app.port')

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
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), status

    def create_blueprint(self, name: str, url_prefix: str, obj: Union[Type[Any], None] = None) -> ApiBlueprint:
        bp: ApiBlueprint = ApiBlueprint(
            name, name, url_prefix=url_prefix, log=self._log)
        bp.register(self, {})

        @bp.errorhandler(404)
        def is_404(e: Exception):
            return App.result(None)

        if obj is not None:
            @bp.rule(rule='/', method='GET', role=[''])
            def get_all():
                return self.result(None)

            @bp.rule(rule='/', method=['POST'], role=[])
            def create_new():
                return self.result(None)

            @bp.rule(rule='/<obj_id>', method=['GET'], role=[])
            def get_one(obj_id: Union[str, int]):
                return self.result(None)

            @bp.rule(rule='/<obj_id>', method=['PUT'], role=[])
            def edit_one(obj_id: Union[str, int]):
                return self.result(None)

            @bp.rule(rule='/<obj_id>', method=['DELETE'], role=[])
            def delete_one(obj_id: Union[str, int]):
                return self.result(None)

        return bp
