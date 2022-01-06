from enum import Enum, auto


class QueryComparison(Enum):
    Eq = auto()         # equal
    Gt = auto()         # greater than
    Gte = auto()        # greater than or equal
    Lt = auto()         # less than
    Lte = auto()        # less than or equal
    Ne = auto()         # not equal
    In = auto()         # in
    NotIn = auto()      # not in
    Like = auto()       # like
    NotLike = auto()    # not like
    IsNull = auto()     # is null
    IsNotNull = auto()  # is not null
    Between = auto()    # between
    Outside = auto()    # not between


class QueryJoin(Enum):
    And = auto()
    Or = auto()
    Not = auto()
    AndNot = auto()
    OrNot = auto()
    Init = auto()
    Close = auto()
    GroupInit = auto()
    GroupClose = auto()


class QueryAction(Enum):
    Create = auto()
    Select = auto()
    Insert = auto()
    Update = auto()
    Delete = auto()


class QueryType(Enum):
    String = auto()
    Int = auto()
    Float = auto()
    Num = auto()
    Date = auto()
    DateTime = auto()
    Time = auto()
    Uuid = auto()
    Id = auto()
    Object = auto()
    Bool = auto()
    List = auto()
    MongoId = auto()


class SqlDialect(Enum):
    SQLITE = auto()
    PGSQL = auto()
    MYSQL = auto()
    ORACLE = auto()
    MSSQL = auto()
    DB2 = auto()
