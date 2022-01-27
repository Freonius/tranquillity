from typing import Generic, TypeVar, Union
from abc import ABC
from ._dtype import DType
from ._nsdtype import NSDType

T = TypeVar('T', bound=DType)
T2 = TypeVar('T2')
NST = TypeVar('NST', bound=NSDType)
