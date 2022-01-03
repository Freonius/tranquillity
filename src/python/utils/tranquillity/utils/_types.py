from typing import Any, Callable, Dict, List, Union, get_type_hints, get_origin, get_args
from functools import wraps
from inspect import FullArgSpec, getfullargspec
from collections.abc import Iterable


def validate_input(obj: Callable, **kwargs) -> None:
    """AI is creating summary for validate_input

    Args:
        obj (Callable): [description]

    Raises:
        TypeError: [description]
    """
    hints: Dict[str, Any] = get_type_hints(obj)
    for attr_name, attr_type in hints.items():
        if attr_name == 'return':
            continue
        if get_origin(attr_type) is Union:
            attr_type = get_args(attr_type)
        if (isinstance(attr_type, Iterable) and Any in attr_type) or attr_type is Any:
            continue
        if not isinstance(kwargs[attr_name], attr_type):
            raise TypeError(f'Argument {attr_name} is not of type {attr_type}')


def type_check(decorator: Callable) -> Callable:
    """AI is creating summary for type_check

    Args:
        decorator (Callable): [description]

    Raises:
        TypeError: [description]

    Returns:
        Callable: [description]
    """
    @wraps(decorator)
    def wrapped_decorator(*args, **kwargs):
        fs_args: FullArgSpec = getfullargspec(decorator)
        func_args: List[str] = fs_args[0]
        kwargs.update(dict(zip(func_args, args)))
        i: int = 0
        # pylint: disable=invalid-name
        a: str
        for a in fs_args.annotations.keys():
            if a == 'return':
                continue
            if a not in kwargs.keys() and \
                    fs_args.defaults is not None and len(fs_args.defaults) > i:
                kwargs.update({a: fs_args.defaults[i]})
                i += 1
        # pylint: enable=invalid-name
        validate_input(decorator, **kwargs)
        return decorator(**kwargs)
    return wrapped_decorator
