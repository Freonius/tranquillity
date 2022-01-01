from functools import wraps, partial
from datetime import datetime
from typing import Any, Callable, List, Optional, Union, Dict
from logging import Logger
from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from ._dataclasses import HttpVerb, Role


class ApiBlueprint(Blueprint):
    _log: Logger

    def __init__(self, name: str, import_name: str, static_folder: Optional[str] = None, static_url_path: Optional[str] = None, template_folder: Optional[str] = None, url_prefix: Optional[str] = None, subdomain: Optional[str] = None, url_defaults: Optional[dict] = None, root_path: Optional[str] = None, cli_group: Optional[str] = None, log: Optional[Logger] = None):
        super().__init__(name, import_name, static_folder=static_folder, static_url_path=static_url_path, template_folder=template_folder,
                         url_prefix=url_prefix, subdomain=subdomain, url_defaults=url_defaults, root_path=root_path, cli_group=cli_group)

        @self.before_request
        def _before():
            pass

        @self.after_request
        def _after(r: Response):
            return Response()

    def rule(self, func: Union[Callable[..., Dict[str, Any]], None] = None, *, rule: str = '/', method: Union[HttpVerb, str, List[HttpVerb], List[str]] = HttpVerb.GET, role: Union[Role, str, List, List[Role], List[str]] = Role.USER, **options: Any):
        if func is None:
            p: partial = partial(self.rule, rule=rule,
                                 method=method, role=role, **options)
            return p

        _methods: List[str] = []
        if isinstance(method, list):
            for x in method:
                if isinstance(x, HttpVerb):
                    _methods.append(x.name)
                else:
                    _methods.append(x.upper())
        if isinstance(method, HttpVerb):
            _methods.append(method.name)
        if isinstance(method, str):
            _methods.append(method.upper())

        @self.route(rule, methods=_methods, strict_slashes=False, **options)
        @wraps(func)
        def _wrapper(*args, **kwargs):
            if func is None:
                raise TypeError
            m: str = str(request.method).upper().strip()
            p: str = ''
            if isinstance(self.url_prefix, str):
                p = self.url_prefix
            if p.endswith('/'):
                p = p[:-1]
            p += rule
            self._log.info(f'{m} {p} :: Started')
            ret: Union[Dict[str, Any], List[Dict[str, Any]], None] = None
            if len(args) == 0 and len(kwargs) == 0:
                ret = func()
            else:
                ret = func(*args, **kwargs)
            self._log.info(f'{m} {p} :: Finished')
            if __debug__:
                self._log.debug(f'{m} {p} :: result={ret}')
            resp: Response = jsonify(
                {
                    'result': ret,
                    'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'message': 'OK',
                    'status': True
                }
            )
            resp.status_code = 200

        return _wrapper
