from typing import Union
from ._dtype import DType


class Text(DType[str]):
    _t = str


class String(Text):
    pass
