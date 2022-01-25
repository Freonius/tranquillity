from typing import Union
from cryptography.fernet import Fernet


class EncryptedString:
    _key: bytes = NotImplemented
    _val: str
    _f = False

    @property
    def value(self) -> str:
        return Fernet(self._key).decrypt(self._val.encode('utf-8')).decode('utf-8')

    @value.setter
    def value(self, val: str) -> None:
        self._val = Fernet(self._key).encrypt(
            val.encode('utf-8')).decode('utf-8')

    @property
    def raw(self) -> str:
        return self._val

    @raw.setter
    def raw(self, val: str) -> None:
        self._val = val

    def __eq__(self, __o: object) -> bool:
        return __o == self.value or __o == self.raw

    def __init__(self, val: str, key: Union[str, bytes, None] = None) -> None:
        if key is None:
            key = Fernet.generate_key()
        if isinstance(key, str):
            key = bytes(key, 'utf-8')
        self._key = key
        self.value = val

    @classmethod
    def from_raw(cls, raw, key):
        c = cls('', key)
        c.raw = raw
        return c

    def __str__(self) -> str:
        return self.raw
