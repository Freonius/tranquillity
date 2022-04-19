from typing import Dict, Union


class Style:
    _attributes: Dict[str, Union[str, int]] = {}
    _predicate: Union[str, None]

    def __init__(self, predicate: Union[str, None], *, width: Union[str, None] = None) -> None:
        self._predicate = predicate
        self.set(width=width)

    def set(self, *, width: Union[str, None] = None) -> 'Style':
        return self

    @property
    def value(self) -> str:
        return ';'.join([f'{key}:{value}' for key, value in self._attributes.items()])
