from abc import ABC, abstractclassmethod, abstractmethod
from typing import Dict, List, Union, Type


class IHtmlElement(ABC):
    _classes: Union[List[str], None] = None
    _children: List['IHtmlElement'] = []
    _id: Union[str, None] = None
    _text: Union[str, None] = None
    _attributes: Dict[str, str] = {}

    def __init__(self, *, children: Union[List['IHtmlElement'], None] = None, text: Union[str, None] = None, id: Union[str, None] = None, classes: Union[List[str], str, None] = None) -> None:
        super().__init__()

    @abstractmethod
    def _is_allowed_child(cls, child: Union['IHtmlElement', Type['IHtmlElement']]) -> bool:
        pass

    @abstractmethod
    def _can_have_children(cls) -> bool:
        pass

    @abstractmethod
    def _can_have_text(cls) -> bool:
        pass

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
    def classes(self) -> List[str]:
        if self._classes is None:
            return []
        return self._classes

    def __getitem__(self, key: str) -> str:
        return self._attributes[key]

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
        return self

    def remove_class(self, class_name: str) -> 'IHtmlElement':
        if self._classes is None:
            return self
        if class_name in self._classes:
            self._classes.remove(class_name)
        return self

    def add_child(self, child: 'IHtmlElement') -> 'IHtmlElement':
        self._children.append(child)
        return self

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
                return self
            _matches.append(self)
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
        if _is_id is True:
            if len(_matches) == 0:
                return None
            return _matches[0]
        return _matches

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return f'<{self.tag} id={self.id} class={" ".join(self.classes)} />'
