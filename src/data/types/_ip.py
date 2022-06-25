from ipaddress import ip_address
from typing import Union
from ._text import Text, NSText
from ...exceptions import ValidationError


class Ip(Text):

    def _more_validation(self) -> None:
        try:
            ip_address(self._value)
        except ValueError as e:
            raise ValidationError('it is not a valid ip') from e
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
                 exclude: bool = False,
                 ) -> None:
        super().__init__(value, field, primary_key, required, default, nullable, json_field,
                         True, None, None, None, None, True, False, False)


class NSIp(NSText):

    def _more_validation(self) -> None:
        try:
            ip_address(self._value)
        except ValueError as e:
            raise ValidationError('it is not a valid ip') from e
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
                 exclude: bool = False,
                 ) -> None:
        super().__init__(value, field, primary_key, required, default, json_field,
                         True, None, None, None, None, True, False, False)
