from typing import List, Union, TypeVar, Type
from bs4 import BeautifulSoup
from .tags._interface import IHtmlElement
from .tags._body import Body
from .tags._html import Html

T = TypeVar('T', bound=IHtmlElement)


class Document:
    _parser: 'HtmlParser'

    def __init__(self, parser: 'HtmlParser') -> None:
        self._parser = parser

    def getElementById(self, id: str) -> IHtmlElement:
        _matches = self._parser.base_tag.find('#' + id)
        if _matches is None:
            raise Exception
        if isinstance(_matches, list):
            if len(_matches) >= 1:
                return _matches[0]
            raise Exception
        return _matches

    def getElementsByClassName(self, class_name: str) -> List[IHtmlElement]:
        pass

    def getElementsByTagName(self, tag: Type[T]) -> List[T]:
        _elements = self._parser.base_tag.find(tag.get_tag_name())
        if _elements is None:
            return []
        if not isinstance(_elements, list):
            _elements = [_elements]
        _out: List[T] = []
        for _x in _elements:
            if isinstance(_x, tag):
                _out.append(_x)
        return _out


class HtmlParser:
    @property
    def body(self) -> Body:
        pass

    @property
    def base_tag(self) -> Html:
        pass

    @property
    def document(self) -> Document:
        return Document(self)

    def __init__(self, content: str) -> None:
        soup: BeautifulSoup = BeautifulSoup(content, 'lxml')

    @staticmethod
    def from_url(url: str) -> 'HtmlParser':
        pass

    @staticmethod
    def from_file(file_name: str) -> 'HtmlParser':
        pass

    @staticmethod
    def new() -> 'HtmlParser':
        pass

    def save(self, file_name: str) -> bool:
        pass
