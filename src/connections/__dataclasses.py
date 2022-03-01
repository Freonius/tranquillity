from typing import Union, Any
from dataclasses import dataclass


@dataclass
class PgColumn:
    column_name: str
    default: Union[None, Any]
    column_type: str
    is_nullable: bool
    is_identity: bool
