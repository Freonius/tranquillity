from abc import ABC
from re import compile, Match
from typing import Dict, List, Pattern, Union, Type


class _IHtmlElement(ABC):
    _classes: Union[List[str], None] = None
    _children: List['IHtmlElement']
    _id: Union[str, None] = None
    _text: Union[str, None] = None
    _attributes: Dict[str, str] = {}
    _can_have_self_closing_tag: bool = False
    _parent: Union['IHtmlElement', None] = None

    def __init__(self,
                 *,
                 children: Union[List['IHtmlElement'], None] = None,
                 text: Union[str, None] = None,
                 id: Union[str, None] = None,
                 classes: Union[List[str], str, None] = None,
                 src: Union[str, None] = None,
                 href: Union[str, None] = None,
                 attributes: Union[Dict[str, str], None] = None,
                 parent: Union['IHtmlElement', None] = None) -> None:
        super().__init__()
        if children is not None:
            self._children = children
        else:
            self._children = []
        self._text = text
        self._id = id
        if isinstance(classes, str):
            classes = [classes]
        self._classes = classes
        self._attributes = {}
        if src is not None:
            self._attributes['src'] = src
        if href is not None:
            self._attributes['href'] = href
        if attributes is not None:
            for _k, _v in attributes.items():
                self._attributes[_k] = _v
        self._parent = parent

    @property
    def parent(self) -> Union['IHtmlElement', None]:
        return self._parent

    @property
    def siblings(self) -> List['IHtmlElement']:
        if self._parent is None:
            return []
        return self._parent.children

    @property
    def href(self) -> Union[str, None]:
        for _k, _v in self._attributes.items():
            if _k.lower().strip() == 'href':
                return _v
        return None

    @href.setter
    def href(self, val: Union[str, None]) -> None:
        if val is None:
            return
        self._attributes['href'] = val

    @property
    def src(self) -> Union[str, None]:
        for _k, _v in self._attributes.items():
            if _k.lower().strip() == 'src':
                return _v
        return None

    @src.setter
    def src(self, val: Union[str, None]) -> None:
        if val is None:
            return
        self._attributes['src'] = val

    @classmethod
    def get_tag_name(cls) -> str:
        return cls.__name__.lower()

    def build_classes(self) -> List[str]:
        return []

    @property
    def tag(self) -> str:
        return self.get_tag_name()

    @property
    def id(self) -> Union[str, None]:
        return self._id

    @id.setter
    def id(self, val: Union[str, None]) -> None:
        self._id = val

    @property
    def has_children(self) -> bool:
        return len(self._children) > 0

    @property
    def children(self) -> List['IHtmlElement']:
        return self._children

    @property
    def num_children(self) -> int:
        return len(self._children)

    @property
    def text(self) -> Union[str, None]:
        return self._text

    @text.setter
    def text(self, val: Union[str, None]) -> None:
        self._text = val

    @property
    def attributes(self) -> Dict[str, str]:
        return self._attributes

    @property
    def classes(self) -> List[str]:
        if self._classes is None:
            return []
        return self._classes

    def __getitem__(self, key: str) -> str:
        return self._attributes[key]

    def __setitem__(self, key: str, attr: str) -> None:
        self._attributes[key] = attr

    def __contains__(self, predicate: object) -> bool:
        if not isinstance(predicate, str):
            return False
        predicate = predicate.strip()
        if predicate.startswith('#'):
            return self._id == predicate.replace('#', '') or any([predicate in child for child in self._children])
        if predicate.startswith('.'):
            return predicate.replace('.', '') in self.classes or any([predicate in child for child in self._children])
        return predicate.lower() == self.tag or any([predicate in child for child in self._children])

    def match(self, predicate: str) -> bool:
        predicate = predicate.strip()
        if predicate.startswith('#'):
            return self._id == predicate.replace('#', '')
        if predicate.startswith('.'):
            return predicate.replace('.', '') in self.classes
        return predicate.lower() == self.tag

    def add_class(self, class_name: str) -> 'IHtmlElement':
        if self._classes is None:
            self._classes = []
        if class_name not in self._classes:
            self._classes.append(class_name)
        return self  # type: ignore

    def remove_class(self, class_name: str) -> 'IHtmlElement':
        if self._classes is None:
            return self  # type: ignore
        if class_name in self._classes:
            self._classes.remove(class_name)
        return self  # type: ignore

    def add_child(self, child: 'IHtmlElement') -> 'IHtmlElement':
        self._children.append(child)
        return self  # type: ignore

    def find(self, predicate: str) -> Union['IHtmlElement', None, List['IHtmlElement']]:
        predicate = predicate.strip()
        _is_id: bool = predicate.startswith('#')
        if not predicate in self:
            if _is_id is True:
                return None
            return []
        _matches: List['IHtmlElement'] = []
        if self.match(predicate):
            if _is_id is True:
                return self  # type: ignore
            _matches.append(self)  # type: ignore
        for child in self._children:
            if not predicate in child:
                continue
            if child.match(predicate):
                if _is_id is True:
                    return child
                _found = child.find(predicate)
                if isinstance(_found, list):
                    _matches.extend(_found)
                elif _found is None:
                    pass
                else:
                    _matches.append(_found)
            else:
                # It's in the children
                _child_match = child.find(predicate)
                if isinstance(_child_match, list):
                    _matches.extend(_child_match)
                elif _child_match is None:
                    continue
                else:
                    _matches.append(_child_match)
        if _is_id is True:
            if len(_matches) == 0:
                return None
            return _matches[0]
        return _matches

    def pattern_match(self, pattern: Union[Pattern, str], *, recursive: bool = False) -> bool:
        if isinstance(pattern, str):
            pattern = compile(pattern)
        _match: Union[Match, None] = None
        if recursive is False:
            if self._text is None:
                return False
            _match = pattern.match(self._text)
            if _match is None:
                return False
            return True
        else:
            if self.pattern_match(pattern, recursive=False) is True:
                return True
            return any([child.pattern_match(pattern, recursive=True) for child in self._children])

    def pattern_find(self, pattern: Union[Pattern, str]) -> List['IHtmlElement']:
        if self.pattern_match(pattern, recursive=True) is False:
            return []
        _matches: List['IHtmlElement'] = []
        if self.pattern_match(pattern, recursive=False):
            _matches.append(self)  # type: ignore
        for child in self._children:
            if not child.pattern_match(pattern, recursive=True):
                continue
            if child.pattern_match(pattern, recursive=False):
                _matches.append(child)
            else:
                # It's in the children
                _child_match = child.pattern_find(pattern)
                if isinstance(_child_match, list) and len(_child_match) > 0:
                    _matches.extend(_child_match)
        return _matches

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        _id_part: str = f' id="{self.id}"' if self.id is not None else ''
        _class_part: str = f' class="{" ".join(self.classes)}"' if len(
            self.classes) > 0 else ''
        _text_part: str = f' text="{self.text}"' if self.text is not None else ''
        _href_part: str = f' href="{self.href}"' if self.href is not None else ''
        _src_part: str = f' src="{self.src}"' if self.src is not None else ''
        return f'<{self.tag}{_id_part}{_class_part}{_text_part}{_href_part}{_src_part} />'


class Text(_IHtmlElement):
    def __repr__(self) -> str:
        return self._text if self._text is not None else ''


class IHtmlElement(_IHtmlElement):
    def add_text(self, text: str) -> 'IHtmlElement':
        self.add_child(Text(text=text, parent=self))  # type: ignore
        return self
