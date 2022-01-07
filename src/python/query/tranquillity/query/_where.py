from typing import Dict, List, Tuple, Type, Union, Any
from json import dumps
from ._enums import QueryComparison, QueryJoin, QueryType, SqlDialect
from ._values import QWhereV, QWhereVR
from ._utils import _fld2sql, _val2sql
from ._dataclasses import WhereCondition
from ._exceptions import QueryFormatError


def _nest_where(data: List[Union[QueryJoin, str, QueryType,
                                 QWhereV, QWhereVR, QueryComparison]]) -> List:
    out: List = []
    _tmp: List[Union[QueryJoin, str, QueryType,
                     QWhereV, QWhereVR, QueryComparison]] = []
    _prev_type: Union[Type, None] = None
    for i, x in enumerate(data):
        if (_prev_type is None or _prev_type is QueryJoin) and isinstance(x, QueryJoin) and x in (QueryJoin.Init, QueryJoin.And, QueryJoin.Or):
            # New Where condition
            _tmp.clear()
            _tmp.append(x)
        elif _prev_type is QueryJoin and len(_tmp) == 1 and isinstance(x, str):
            # Append field name
            _tmp.append(x)
        elif _prev_type is str and len(_tmp) == 2 and isinstance(x, QueryType):
            # Append Type
            _tmp.append(x)
        elif _prev_type is QueryType and len(_tmp) == 3 and isinstance(x, QueryComparison):
            # Append comparison
            _tmp.append(x)
        elif _prev_type is QueryComparison and len(_tmp) == 4 and isinstance(x, (QWhereV, QWhereVR)):
            # Append value
            _tmp.append(x)
        elif _prev_type in (QWhereV, QWhereVR) and len(_tmp) == 5 and isinstance(x, QueryJoin) and x is QueryJoin.Close:
            # End where condition
            if not isinstance(_tmp[0], QueryJoin):
                raise QueryFormatError
            if not isinstance(_tmp[1], str):
                raise QueryFormatError
            if not isinstance(_tmp[2], QueryType):
                raise QueryFormatError
            if not isinstance(_tmp[3], QueryComparison):
                raise QueryFormatError
            if not isinstance(_tmp[4], (QWhereV, QWhereVR)):
                raise QueryFormatError
            _wc: WhereCondition = WhereCondition(
                join=_tmp[0],
                field=_tmp[1],
                type=_tmp[2],
                comparison=_tmp[3],
                value=_tmp[4]
            )
            out.append(_wc)
            _tmp.clear()
        elif (_prev_type is None or _prev_type is QueryJoin) and isinstance(x, QueryJoin) and x is QueryJoin.GroupInit:
            try:
                out.append(_nest_where(
                    data[i:data.index(QueryJoin.GroupClose, i)]))
            except ValueError as e:
                raise QueryFormatError('Group not closed') from e
        else:
            raise QueryFormatError
        _prev_type = type(x)
    return out


def _wc2sql(wcs: List, dialect: SqlDialect, prev_data: Union[Dict[str, str], None] = None, prev_list_data: Union[List[str], None] = None) -> Tuple[str, Dict[str, str], Tuple[str, ...]]:
    out: str = ''
    params: Dict[str, str] = {}
    list_params: List[str] = []
    if prev_data is not None:
        params = prev_data
    if prev_list_data is not None:
        list_params = prev_list_data.copy()
    for wc in wcs:
        _tmp: str = ''
        if isinstance(wc, WhereCondition):
            if wc.join is QueryJoin.And and len(out) > 0:
                _tmp += 'AND '
            elif wc.join is QueryJoin.Or and len(out) > 0:
                _tmp += 'OR '
            elif wc.join is QueryJoin.AndNot and len(out) > 0:
                _tmp += 'AND NOT '
            elif wc.join is QueryJoin.OrNot and len(out) > 0:
                _tmp += 'OR NOT '
            _tmp += f'{_fld2sql(wc.field, dialect)} '
            if wc.comparison is QueryComparison.Eq:
                _tmp += '= '
            elif wc.comparison is QueryComparison.Ne:
                _tmp += '<> '
            elif wc.comparison is QueryComparison.Gt:
                _tmp += '> '
            elif wc.comparison is QueryComparison.Gte:
                _tmp += '>= '
            elif wc.comparison is QueryComparison.Lt:
                _tmp += '< '
            elif wc.comparison is QueryComparison.Lte:
                _tmp += '<= '
            elif wc.comparison is QueryComparison.IsNull:
                _tmp += 'IS NULL '
                out += _tmp
                continue
            elif wc.comparison is QueryComparison.IsNotNull:
                _tmp += 'IS NOT NULL '
                out += _tmp
                continue
            elif wc.comparison is QueryComparison.Between:
                _tmp += 'BETWEEN '
            elif wc.comparison is QueryComparison.Outside:
                _tmp += 'NOT BETWEEN '
            # Add to params
            _field: str = ''
            _field1: str = ''
            _field2: str = ''
            if isinstance(wc.value, QWhereV):
                if wc.field in params.keys():
                    _i: int = 0
                    while True:
                        if f'{wc.field}{_i}' not in params.keys():
                            _field = f'{wc.field}{_i}'
                            break
                        _i += 1
                    del _i
                else:
                    _field = wc.field
                if wc.value._val is None:
                    raise QueryFormatError
                _val: str = _val2sql(wc.value._val, dialect)
                list_params.append(_val)
                params[_field] = _val
                del _val
            else:
                _j: int = 0
                while True:
                    if f'{wc.field}{_j}' not in params.keys() and f'{wc.field}{_j + 1}' not in params.keys():
                        _field1 = f'{wc.field}{_j}'
                        _field2 = f'{wc.field}{_j + 1}'
                        break
                    _j += 1
                if len(wc.value._val) > 2:
                    raise QueryFormatError
                if wc.value._val[0] is None or wc.value._val[1] is None:
                    raise QueryFormatError
                _val1: str = _val2sql(wc.value._val[0], dialect)
                _val2: str = _val2sql(wc.value._val[1], dialect)
                params[_field1] = _val1
                params[_field2] = _val2
                list_params.append(_val1)
                list_params.append(_val2)
                del _val1, _val2
            # Prepared params
            if dialect is SqlDialect.PGSQL:
                if isinstance(wc.value, QWhereV):
                    _tmp += f'%({_field})s '
                elif wc.comparison in (QueryComparison.Between, QueryComparison.Outside) and isinstance(wc.value, QWhereVR):
                    _tmp += f'%({_field1})s AND %({_field2})s '
            elif dialect is SqlDialect.MYSQL:
                raise NotImplementedError
                if isinstance(wc.value, QWhereV):
                    _tmp += f'%({_field})s '
                elif wc.comparison in (QueryComparison.Between, QueryComparison.Outside) and isinstance(wc.value, QWhereVR):
                    _tmp += f'%({_field1})s AND %({_field2})s '
            elif dialect is SqlDialect.MSSQL:
                raise NotImplementedError
                if isinstance(wc.value, QWhereV):
                    _tmp += f'%({_field})s '
                elif wc.comparison in (QueryComparison.Between, QueryComparison.Outside) and isinstance(wc.value, QWhereVR):
                    _tmp += f'%({_field1})s AND %({_field2})s '
            elif dialect is SqlDialect.SQLITE:
                if isinstance(wc.value, QWhereV):
                    _tmp += f'? '
                elif wc.comparison in (QueryComparison.Between, QueryComparison.Outside) and isinstance(wc.value, QWhereVR):
                    _tmp += f'? AND ? '
            elif dialect is SqlDialect.ORACLE:
                raise NotImplementedError
                if isinstance(wc.value, QWhereV):
                    _tmp += f'%({_field})s '
                elif wc.comparison in (QueryComparison.Between, QueryComparison.Outside) and isinstance(wc.value, QWhereVR):
                    _tmp += f'%({_field1})s AND %({_field2})s '
            elif dialect is SqlDialect.DB2:
                raise NotImplementedError
                if isinstance(wc.value, QWhereV):
                    _tmp += f'%({_field})s '
                elif wc.comparison in (QueryComparison.Between, QueryComparison.Outside) and isinstance(wc.value, QWhereVR):
                    _tmp += f'%({_field1})s AND %({_field2})s '
            out += _tmp
        elif isinstance(wc, list):
            _tmp_tuple: Tuple[str, ...]
            _tmp, params, _tmp_tuple = _wc2sql(
                wc, dialect, params, list_params)
            for _x in _tmp_tuple:
                list_params.append(_x)
            out += _tmp
        del _tmp
    return (out, params, tuple(list_params))


def _wc2es(wcs: List, prev_data: Union[Dict[str, str], None] = None, prev_list_data: Union[List[str], None] = None) -> Tuple[str, Dict[str, str], Tuple[str, ...]]:
    if len(wcs) == 0 and prev_data is None and prev_list_data is None:
        return dumps({'query': {'match_all': {}}}), {}, ()
    if len(wcs) == 1 and isinstance(wcs[0], WhereCondition):
        pass
    _wcs: List[WhereCondition] = []

    def _unlist(_l: List, _d: List[WhereCondition]) -> None:
        for _e in _l:
            if isinstance(_e, WhereCondition):
                _d.append(_e)
            elif isinstance(_e, list):
                _unlist(_e, _d)
    _unlist(wcs, _wcs)
    del _unlist

    body: Dict[str, Dict[str, Any]] = {'query': {}}
    _must: int = len(list(filter(lambda _wc: isinstance(
        _wc, WhereCondition)
        and _wc.join in (QueryJoin.Init, QueryJoin.And), _wcs)))
    _should: int = len(list(filter(lambda _wc: isinstance(
        _wc, WhereCondition)
        and _wc.join is QueryJoin.Or, _wcs)))
    _must_not: int = len(list(filter(lambda _wc: isinstance(
        _wc, WhereCondition)
        and _wc.join is QueryJoin.AndNot, _wcs)))
    _should_not: int = len(list(filter(lambda _wc: isinstance(
        _wc, WhereCondition)
        and _wc.join is QueryJoin.OrNot, _wcs)))

    if _must == 1:
        body['query']['must'] = {}
    elif _must > 1:
        body['query']['must'] = []

    del _must

    if _should == 1:
        body['query']['should'] = {}
    elif _should > 1:
        body['query']['should'] = []

    del _should

    if _must_not == 1:
        body['query']['must_not'] = {}
    elif _must_not > 1:
        body['query']['must_not'] = []

    del _must_not

    if _should_not == 1:
        body['query']['should_not'] = {}
    elif _should_not > 1:
        body['query']['should_not'] = []

    del _should_not

    for wc in _wcs:
        _query: Dict[str, Any] = {}
        if wc.comparison is QueryComparison.Eq:
            _query['match'] = {wc.field: wc.value._val}
        elif wc.comparison is QueryComparison.Like:
            _query['regexp'] = {wc.field: {'value': wc.value._val}}
        elif wc.comparison is QueryComparison.Ne:
            _query['match'] = {wc.field: wc.value._val}
        elif wc.comparison is QueryComparison.Gt:
            _query['range'] = {wc.field: {'gt': wc.value._val}}
        elif wc.comparison is QueryComparison.Gte:
            _query['range'] = {wc.field: {'gte': wc.value._val}}
        elif wc.comparison is QueryComparison.Lt:
            _query['range'] = {wc.field: {'lt': wc.value._val}}
        elif wc.comparison is QueryComparison.Lte:
            _query['range'] = {wc.field: {'lte': wc.value._val}}
        elif wc.comparison is QueryComparison.IsNull:
            pass    # es has no is null?
        elif wc.comparison is QueryComparison.IsNotNull:
            pass    # es has not is null?
        elif wc.comparison is QueryComparison.Between:
            if isinstance(wc.value, QWhereVR):
                _query['range'] = {wc.field: {
                    'gte': wc.value._val[0], 'lte': wc.value._val[1]}}
        elif wc.comparison is QueryComparison.Outside:
            if isinstance(wc.value, QWhereVR):
                _query['range'] = {wc.field: {
                    'gte': wc.value._val[1], 'lte': wc.value._val[0]}}

        # Append to body
        if wc.join in (QueryJoin.Init, QueryJoin.And):
            pass  # must
        elif wc.join is QueryJoin.Or:
            pass  # should
        elif wc.join is QueryJoin.AndNot:
            pass  # must not
        elif wc.join is QueryJoin.OrNot:
            pass  # should not
