from typing import Union
from phonenumbers import parse, NumberParseException
from ._text import Text, NSText
from ...exceptions import ValidationError


class PhoneNumber(Text):
    def _more_validation(self) -> None:
        try:
            parse(self._value)
        except NumberParseException as e:
            raise ValidationError('invalid phone number') from e
        super()._more_validation()

    def __init__(self, value: Union[str, None] = None, field: Union[str, None] = None, primary_key: bool = False, required: bool = True, default: Union[str, None] = None, nullable: bool = True, json_field: Union[str, None] = None, not_empty: bool = False) -> None:
        super().__init__(value, field, primary_key, required, default, nullable,
                         json_field, True, None, None, None, None, True, False, False)


class NSPhoneNumber(NSText):
    def _more_validation(self) -> None:
        try:
            parse(self._value)
        except NumberParseException as e:
            raise ValidationError('invalid phone number') from e
        super()._more_validation()

    def __init__(self, value: Union[str, None] = None, field: Union[str, None] = None, primary_key: bool = False, required: bool = True, default: Union[str, None] = None, json_field: Union[str, None] = None, not_empty: bool = False) -> None:
        super().__init__(value, field, primary_key, required, default,
                         json_field, True, None, None, None, None, True, False, False)
