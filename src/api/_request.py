from typing import Any, Dict, Set
from flask import request
from ._dataclasses import HttpVerb

class Request(object):
    _headers: Dict[str, str] = {}
    _data: Dict[str, Any] = {}
    _file_keys: Set[str] = set([])
    _method: HttpVerb
    _path: str

    def __init__(self, decrypt: bool = False) -> None:
        if request.headers is None:
            self._headers = {}
        else:
            self._headers = { str(k).lower().strip(): str(v).strip() for k, v in dict(request.headers).items() }

    def __str__(self) -> str:
        n: str = self.__class__.__name__
        if __debug__:
            return f'<{n} {self._method.value}::{self._path} headers={self._headers}; data={self._data}>'
        return f'<{n} {self._method.value}::{self._path}>'
        
    @property
    def headers(self) -> Dict[str, str]:
        return self._headers

class Response(object):
    def __init__(self, encrypt: bool = False) -> None:
        pass

