from typing import Type, TypeVar, Union, Iterable, Generic

T = TypeVar('T')


class Array(list, Generic[T]):
    _t: Type[T]

    def __init__(self, t: Type[T], el: Union[Iterable[T], None] = None) -> None:
        self._t = t
        super().__init__()
        if el is not None:
            for e in el:
                if not isinstance(e, self._t):
                    raise TypeError('Here')
            self.extend(el)

    @property
    def get_generic(self) -> Type[T]:
        return self._t

    def append(self, __object: T) -> None:
        if not isinstance(__object, self._t):
            raise TypeError
        return super().append(__object)

    def extend(self, __iterable: Iterable[T]) -> None:
        for e in __iterable:
            if not isinstance(e, self._t):
                raise TypeError
        return super().extend(__iterable)

    def uniques(self) -> Iterable[T]:
        return list(set(self))

    def distincts(self) -> Iterable[T]:
        return self.uniques()
