from typing import TypeVar, TYPE_CHECKING, Union, Iterable
from bson import ObjectId
from ..query._dataclasses import WhereCondition

if TYPE_CHECKING is True:
    from ..data._dataobject import DataObject

T = TypeVar('T', bound='DataObject')
IdType = Union[int, str, ObjectId, None]
WhereType = Union[Iterable[WhereCondition], None]
