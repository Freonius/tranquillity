from abc import ABC, abstractmethod
from typing import List, Union
from ..html.tags._interface import IHtmlElement


class Widget(ABC):
    _child: Union['Widget', None, List['Widget']] = None

    def __init__(self, *, child: Union['Widget', None, List['Widget']] = None) -> None:
        self._child = child

    @abstractmethod
    def html(self) -> IHtmlElement:
        pass
