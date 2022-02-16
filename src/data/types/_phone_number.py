from typing import Union
from phonenumbers import parse, NumberParseException
from ._text import Text, NSText
from ...exceptions import ValidationError


class PhoneNumber(Text):
    def _more_validation(self) -> None:
        if self._value is None:
            return
        try:
            parse(self._value)
        except NumberParseException as e:
            raise ValidationError('invalid phone number') from e
        super()._more_validation()

    def __init__(self,
                 value: Union[str, None] = None,
                 field: Union[str, None] = None,
                 primary_key: bool = False,
                 required: bool = True,
                 default: Union[str, None] = None,
                 nullable: bool = True,
                 json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False,) -> None:
        super().__init__(value, field=field, primary_key=primary_key, required=required, default=default,
                         json_field=json_field, not_empty=True,
                         indexable=indexable, filterable=filterable, exclude=exclude, nullable=nullable)


class NSPhoneNumber(NSText):
    def _more_validation(self) -> None:
        try:
            parse(self._value)
        except NumberParseException as e:
            raise ValidationError('invalid phone number') from e
        super()._more_validation()

    def __init__(self,
                 value: Union[str, None] = None,
                 field: Union[str, None] = None,
                 primary_key: bool = False,
                 required: bool = True,
                 default: Union[str, None] = None,
                 json_field: Union[str, None] = None,
                 indexable: bool = True,
                 filterable: bool = True,
                 exclude: bool = False,) -> None:
        super().__init__(value, field=field, primary_key=primary_key, required=required, default=default,
                         json_field=json_field, not_empty=True,
                         indexable=indexable, filterable=filterable, exclude=exclude)
