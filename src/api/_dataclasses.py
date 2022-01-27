from enum import Enum, auto
from dataclasses import dataclass
from typing import Union, Iterable, Tuple


class HttpVerb(Enum):
    HEAD = 'HEAD'
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Role(Enum):
    MACHINE = auto()
    SUPERADMIN = auto()
    ADMIN = auto()
    USER = auto()
    NOT_LOGGED = auto()


@dataclass
class ApiAddr:
    verb: HttpVerb
    protocol: str
    address: str
    port: Union[int, None]
    access_token_key: Union[None, str]
    access_token_value: Union[None, str]
    path: str
    variables: Union[None, Iterable[Tuple[str, Union[int, str]]]]
    returns_list: bool
