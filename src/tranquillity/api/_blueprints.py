from typing import Any, Callable, List, Optional, Union, Literal
from logging import Logger
from flask import Blueprint, jsonify
from ._dataclasses import HttpVerb, Role

EmptyList = Literal['']
EmptyList.__args__ = []  # type: ignore[attr-defined]
class ApiBlueprint(Blueprint):
    def __init__(self, name: str, import_name: str, static_folder: Optional[str] = None, static_url_path: Optional[str] = None, template_folder: Optional[str] = None, url_prefix: Optional[str] = None, subdomain: Optional[str] = None, url_defaults: Optional[dict] = None, root_path: Optional[str] = None, cli_group: Optional[str] = None, log: Optional[Logger] = None):
        super().__init__(name, import_name, static_folder=static_folder, static_url_path=static_url_path, template_folder=template_folder, url_prefix=url_prefix, subdomain=subdomain, url_defaults=url_defaults, root_path=root_path, cli_group=cli_group)

    def rule(self, rule: str, method: Union[HttpVerb, str, List[HttpVerb], List[str]], role: Union[Role, str, List, List[Role], List[str]] = Role.NOT_LOGGED, **options: Any) -> Callable:
        if 'strict_slashes' not in options.keys():
            options['strict_slashes'] = False
        def unauthorized(f: Callable) -> Callable:
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return lambda: (jsonify({'status': False, 'message': 'Unauthorized', 'result': None}), 401)
        roles: List[Role] = []
        if 'roles' in options.keys():
            if isinstance(options['roles'], list) and all([isinstance(x, str) for x in options['roles']]):
                roles = options['roles']
        if ('requires_auth' in options.keys() and isinstance(options['requires_auth'], bool) and options['requires_auth'] is True) or len(roles) > 0:
            if len(roles) == 0:
                return unauthorized
        
        return super().route(rule, **options)
