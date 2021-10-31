# pylint: disable=missing-module-docstring,missing-class-docstring

class ConnectionException(Exception):
    pass

class ValidationError(Exception):
    pass

class NotAllowedOperation(Exception):
    pass

class ConversionError(ValueError):
    pass