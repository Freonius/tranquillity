from re import compile, Pattern, RegexFlag, match, Match
from typing import Dict, List, Union
from dataclasses import dataclass


@dataclass
class LinkParts:
    protocol: Union[str, None]
    username: Union[str, None]
    password: Union[str, None]
    domain: str
    port: Union[int, None]
    path: Union[List[str], None]
    params: Union[Dict[str, str], None]
    anchor: Union[str, None] = None


LINK: Pattern[str] = compile(
    r"^\s*((?:https?|wss|git|ssh)://)?([a-zA-Z_0-9-%]+(?:\:[a-zA-Z_0-9-%]+)?\@)?((?:[0-9\.])+|(?:(?:www\.)?[a-zA-Z_\.0-9-]+(?:\.[a-zA-Z]+)))(?:\:([0-9]+))?(/[a-zA-Z/_\.0-9-]*)?(\?[a-zA-Z_\.0-9-=%&]*)?$", flags=RegexFlag.M)


def is_link(input: str) -> bool:
    m: Union[Match, None] = match(LINK, input.strip())
    return m is not None


def parse_link(input: str) -> Union[LinkParts, None]:
    m: Union[Match, None] = match(LINK, input)
    if m is None:
        return None
    _protocol: Union[str, None] = m.group(1)
    _up: Union[str, None] = m.group(2)
    _dom: Union[str, None] = m.group(3)
    _prt: Union[str, None] = m.group(4)
    _pth: Union[str, None] = m.group(5)
    _prm: Union[str, None] = m.group(6)
    del m
    _u: Union[str, None] = None
    _p: Union[str, None] = None
    if _up is not None:
        _up = _up[:-1]
        _u = _up.split(':')[0]
        if len(_up.split(':')) == 2:
            _p = _up.split(':')[1]
    del _up
    if _protocol is not None:
        _protocol = _protocol[:-3]
    if _dom is None:
        _dom = ''
    return LinkParts(
        protocol=_protocol,
        username=_u,
        password=_p,
        domain=_dom,
        port=int(_prt) if _prt is not None else None,
        path=[x for x in _pth.split('/') if x !=
              ''] if _pth is not None else None,
        params={k.split('=')[0]: k.split('=')[1] for k in [x.replace(
            '?', '') for x in _prm.split('&')]} if _prm is not None else None
    )
