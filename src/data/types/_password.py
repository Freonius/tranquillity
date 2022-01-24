from cryptography.fernet import Fernet
from typing import Union, Callable
from re import Pattern
from ._text import Text, NSText


class Password(Text):
    pass


class NSPassword(NSText):
    pass
