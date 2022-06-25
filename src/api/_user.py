from typing import Dict
from ..data._dataobject import DataObject
from ..data.types._text import NSString


class User(DataObject):
    __permissions__: Dict[str, str] = {
        'GET': 'machine',
        'POST': 'public',
        'PUT': 'user.self',
        'DELETE': 'user.self;superadmin'
    }
    first_name = NSString(json_field='firstName', not_empty=True)
    last_name = NSString(json_field='lastName', not_empty=True)
    role = NSString(json_field='role', not_empty=True, default='user')
