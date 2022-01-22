from typing import Union

from dataclasses import dataclass
from ._enums import QueryComparison, QueryJoin, QueryType
from ._values import QWhereV, QWhereVR


@dataclass
class WhereCondition:
    join: QueryJoin
    field: str
    type: QueryType
    comparison: QueryComparison
    value: Union[QWhereV, QWhereVR]


@dataclass
class Table:
    table: str
    schema: Union[str, None] = None
    db: Union[str, None] = None
