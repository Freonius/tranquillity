from typing import Any, Dict, List, Union

from ._enums import QueryAction, QueryComparison, QueryJoin, QueryType
from ._values import QWhereV, QWhereVR
from ._select import QSelect


class Q_:
    _where: List[Union[QueryJoin, str, QueryType,
                       QWhereV, QWhereVR, QueryComparison]]
    _action: QueryAction
    _table: str
    _schema: Union[str, None]
    _fields: Union[List[str], None]
    _data: Union[Dict[str, Any], None]

    def __init__(self, action: QueryAction) -> None:
        self._action = action
        self._where = []

    def _add_where_bit(self, bit: Union[QueryJoin, str, QueryType,
                       QWhereV, QWhereVR, QueryComparison]) -> None:
        self._where.append(bit)

    @staticmethod
    def Select(*fields: str, from_table: str, with_schema: Union[str, None] = None) -> 'QSelect':
        return QSelect(Q_(QueryAction.Select))

    @staticmethod
    def Insert(data: Dict[str, Any], into_table: str, with_schema: Union[str, None] = None) -> None:
        pass

    @staticmethod
    def Update(data: Dict[str, Any], from_table: str, with_schema: Union[str, None] = None) -> None:
        pass

    @staticmethod
    def Delete(from_table: str, with_schema: Union[str, None] = None) -> None:
        pass

    @staticmethod
    def Create(table: str, with_schema: Union[str, None] = None) -> None:
        pass

    def __getitem__(self, key: str) -> str:
        pass
