from pytest import raises
from ._fixture import *


def test_logger(fld):
    from ..tranquillity.logger import CustomLogger
    log = CustomLogger()
