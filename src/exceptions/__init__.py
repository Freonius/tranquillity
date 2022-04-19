# pylint: disable=missing-module-docstring,missing-class-docstring
from re import findall


class ConnectionException(Exception):
    pass


class ValidationError(Exception):
    pass


class NotAllowedOperation(Exception):
    pass


class ConversionError(ValueError):
    pass


class SSHException(Exception):
    pass


class HttpException(Exception):
    _status_code: int = 500

    @property
    def reason(self) -> str:
        _cname: str = self.__class__.__name__.replace('Exception', '')
        return ' '.join(findall('[A-Z][^A-Z]*', _cname)).strip()

    @property
    def status_code(self) -> int:
        return self._status_code


class BadRequestException(HttpException):
    _status_code = 400


class UnauthorizedException(HttpException):
    _status_code = 401


class PaymentRequiredException(HttpException):
    _status_code = 402


class ForbiddenException(HttpException):
    _status_code = 403


class NotFoundException(HttpException):
    _status_code = 404


class ResourceNotFoundException(HttpException):
    _status_code = 404


class MethodNotAllowedException(HttpException):
    _status_code = 405


class NotAcceptableException(HttpException):
    _status_code = 406


class ProxyAuthenticationRequiredException(HttpException):
    _status_code = 407


class RequestTimeoutException(HttpException):
    _status_code = 408


class ConflictException(HttpException):
    _status_code = 409


class GoneException(HttpException):
    _status_code = 410


class LengthRequiredException(HttpException):
    _status_code = 411


class PreconditionFailedException(HttpException):
    _status_code = 412


class PayloadTooLargeException(HttpException):
    _status_code = 413


class UriTooLongException(HttpException):
    _status_code = 414


class UnsupportedMediaTypeException(HttpException):
    _status_code = 415


class RangeNotSatisfiableException(HttpException):
    _status_code = 416


class ExpectationFailedException(HttpException):
    # This is passive-aggressive
    _status_code = 417


class WhatTheFuckException(HttpException):
    _status_code = 418


class MisdirectedRequestException(HttpException):
    _status_code = 421


class UnprocessableEntityException(HttpException):
    _status_code = 422


class LockedException(HttpException):
    _status_code = 423


class FailedDependencyException(HttpException):
    _status_code = 424


class TooEarlyException(HttpException):
    # There's a sexual joke, here, somewhere
    _status_code = 425


class UpgradeRequiredException(HttpException):
    _status_code = 426


class PreconditionRequiredException(HttpException):
    _status_code = 428


class TooManyRequestsException(HttpException):
    _status_code = 429


class RequestHeaderFieldsTooLargeException(HttpException):
    _status_code = 431


class UnavailableForLegalReasonsException(HttpException):
    # This is my favourite!
    _status_code = 451


class InternalServerErrorException(HttpException):
    # No, THIS is my favourite
    _status_code = 500


class NotImplementedException(HttpException):
    _status_code = 501


class BadGatewayException(HttpException):
    _status_code = 502


class ServiceUnavailableException(HttpException):
    _status_code = 503


class GatewayTimeoutException(HttpException):
    _status_code = 504


class HttpVersionNotSupportedException(HttpException):
    _status_code = 505


class VariantAlsoNegotatesException(HttpException):
    _status_code = 506


class InsufficientStorageException(HttpException):
    _status_code = 507


class LoopDetectedException(HttpException):
    _status_code = 508


class NotExtendedException(HttpException):
    _status_code = 510


class NetworkAuthenticationRequiredException(HttpException):
    _status_code = 511
