from pytest import raises


def test_exceptions():
    from ..src.exceptions import ConnectionException, \
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
