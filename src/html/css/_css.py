from typing import Dict, Union


class Style:
    _attributes: Dict[str, Union[str, int]] = {}
    _predicate: Union[str, None]

    def __init__(self,
                 predicate: Union[str, None] = None,
                 **kwargs: str) -> None:
        self._predicate = predicate
        for _k, _v in kwargs.items():
            self[_k] = _v

    def set(self, *, width: Union[str, None] = None) -> 'Style':
        return self

    def __getitem__(self, key: str) -> str:
        return str(self._attributes[key])

    def __setitem__(self, key: str, val: str) -> None:
        self._attributes[key] = val

    @property
    def value(self) -> str:
        return ';'.join([f'{key}:{value}' for key, value in self._attributes.items()])

    @staticmethod
    def inline_parse(style: str) -> 'Style':
        _attrs: Dict[str, str] = {}
        for _split in style.split(';'):
            _pred = _split.split(':')
            if len(_pred) == 2:
                _attrs[_pred[0].strip()] = _pred[1].strip()
        return Style(None, **_attrs)
