from typing import Union, Type
from ._interface import IHtmlElement


class Html(IHtmlElement):
    def _is_allowed_child(cls, child: Union['IHtmlElement', Type['IHtmlElement']]) -> bool:
        return child.get_tag_name() in ('head', 'body')

    def _can_have_children(cls) -> bool:
        return True

    def _can_have_text(cls) -> bool:
        return False
