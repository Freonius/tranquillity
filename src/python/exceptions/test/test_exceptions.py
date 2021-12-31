from sys import path
from os.path import realpath, dirname, sep
from pytest import raises
path.append(realpath(dirname(__file__) +
            f'{sep}..'))


def test_exceptions():
    from ..tranquillity.exceptions import ConnectionException, \
        ValidationError, \
        NotAllowedOperation, \
        ConversionError, \
        UnauthorizedException

    def e1(t):
        if 1 == 1:
            raise t

    with raises(ConnectionException):
        e1(ConnectionException)

    with raises(ValidationError):
        e1(ValidationError)

    with raises(NotAllowedOperation):
        e1(NotAllowedOperation)

    with raises(ConversionError):
        e1(ConversionError)

    try:
        raise UnauthorizedException
    except UnauthorizedException as e:
        assert e.reason == 'Unauthorized'
        assert e.status_code == 401
