from ...src.data._dataobject import DataObject
from ...src.data.types._date import NSDate, Date
from ...src.data.types._datetime import NSDateTime
from ...src.data.types._text import String, NSString
from ...src.data.types._int import NSInt
from ...src.data.types._id import StrId
from ...src.connections._elasticsearch import Elasticsearch


class President(DataObject):
    __conn__ = Elasticsearch

    id = StrId()
    first_name = NSString(not_empty=True)
    last_name = NSString(not_empty=True)
    term_start = NSDate()
    term_end = Date()
    created = NSDateTime(default='now')
    order = NSInt(greater_than_zero=True)
