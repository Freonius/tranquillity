# pylint: disable=missing-module-docstring,missing-class-docstring

class ConnectionException(Exception):
    pass


class ValidationError(Exception):
    pass


class NotAllowedOperation(Exception):
    pass


class ConversionError(ValueError):
    pass


class HttpException(Exception):
    _explanation: str = 'Base Http Exception'
    _status_code: int = 500

    @property
    def explanation(self) -> str:
        return self._explanation

    @property
    def status_code(self) -> int:
        return self._status_code


class UnauthorizedException(HttpException):
    _explanation = 'Unauthorized'
    _status_code = 401
