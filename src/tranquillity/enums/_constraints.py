from enum import Enum, auto

class Constraints(Enum):
    not_empty = auto()
    greater_than_0 = auto()
    not_null = auto()
    is_email = auto()
    is_uri = auto()
    after_now = auto()
    before_now = auto()
    
