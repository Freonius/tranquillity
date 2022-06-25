from typing import List, Union, TypeVar, Type
from bs4 import BeautifulSoup, NavigableString, Tag
from .tags import ALL_TAGS, Body, Html, IHtmlElement

T = TypeVar('T', bound=IHtmlElement)


class Document:
    _parser: 'HtmlParser'

    def __init__(self, parser: 'HtmlParser') -> None:
        self._parser = parser

    def getElementById(self, id: str) -> IHtmlElement:
        _matches = self._parser.html.find('#' + id)  # type: ignore
        if _matches is None:
            raise Exception
        if isinstance(_matches, list):
            if len(_matches) >= 1:
                return _matches[0]  # type: ignore
            raise Exception
        return _matches  # type: ignore

    def getElementsByClassName(self, class_name: str) -> List[IHtmlElement]:
        _elements = self._parser.html.find('.' + class_name)  # type: ignore
        if _elements is None:
            return []
        if not isinstance(_elements, list):
            _elements = [_elements]
        return _elements  # type: ignore

    def getElementsByTagName(self, tag: Type[T]) -> List[T]:
        _elements = self._parser.html.find(tag.get_tag_name())  # type: ignore
        if _elements is None:
            return []
        if not isinstance(_elements, list):
            _elements = [_elements]
        _out: List[T] = []
        for _x in _elements:
            if isinstance(_x, tag):
                _out.append(_x)
        return _out

    def getElementByText(self, pattern: str) -> List[IHtmlElement]:
        return self._parser.html.pattern_find(pattern)  # type: ignore


def _parse(tag: Union[Tag, NavigableString], parent: Union[IHtmlElement, None]) -> Union[Html, None]:
    if isinstance(tag, NavigableString):
        if parent is None:
            raise Exception
        parent.add_text(tag.text)
    else:
        tag_name: str = tag.name.lower().strip()
        _tag: Union[IHtmlElement, None] = None
        if tag_name in ALL_TAGS.keys():
            _tag = ALL_TAGS[tag_name](parent=parent)
        if _tag is not None:
            for _k, _v in tag.attrs.items():
                if _k.lower().strip() == 'id':
                    _tag.id = _v
                elif _k.lower().strip() == 'class':
                    if isinstance(_v, str):
                        for _c in _v.split(' '):
                            _tag.add_class(_c)
                    elif isinstance(_v, list):
                        for _cl in _v:
                            if isinstance(_cl, str):
                                _tag.add_class(_cl)
                else:
                    _tag[_k] = _v
            for child in tag.children:
                _parse(child, _tag)
            if parent is None and isinstance(_tag, Html):
                return _tag
            if parent is None:
                raise Exception
            parent.add_child(_tag)
    return None


class HtmlParser:
    _html: Html

    @property
    def body(self) -> Body:
        _bds = self.document.getElementsByTagName(Body)
        if len(_bds) == 1:
            return _bds[0]
        raise Exception

    @property
    def html(self) -> Html:
        return self._html

    @property
    def document(self) -> Document:
        return Document(self)

    def __init__(self, content: str) -> None:
        soup: BeautifulSoup = BeautifulSoup(content, 'lxml')
        node: Union[Tag, NavigableString]
        html: Union[Html, None] = None
        for node in soup.find_all('html', recursive=True):
            html = _parse(node, html)
        if isinstance(html, Html):
            self._html = html
        else:
            raise Exception

    @staticmethod
    def from_url(url: str) -> 'HtmlParser':
        pass

    @staticmethod
    def from_file(file_name: str) -> 'HtmlParser':
        with open(file_name, 'r', encoding='utf-8') as _f:
            return HtmlParser(_f.read())

    @staticmethod
    def new() -> 'HtmlParser':
        return HtmlParser('<!DOCTYPE html><html><body></body></html>')

    def save(self, file_name: str, doc_type: str = 'html') -> bool:
        pass
