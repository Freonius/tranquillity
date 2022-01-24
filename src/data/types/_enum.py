from abc import ABCMeta
from enum import auto
from ._nsdtype import NSDType
from .._dataobject import DataObject


class Enum(NSDType[str]):
    _t = str

    def __get__(self, instance, owner: ABCMeta) -> str:
        # TODO
        if owner is DataObject:
            print('HERE')
            return list([x for x in owner.get_fields_tuple() if x is self])[0].value

        if instance is None:
            return self
        if hasattr(instance, '__getitem__'):
            try:
                out = instance[self._field]
                if isinstance(out, self._t) or out is None:
                    return out
            except Exception:
                pass
        return self.value
