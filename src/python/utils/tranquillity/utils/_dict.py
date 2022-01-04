"""Module for flattening and unflattening a dictionary.

```python
d {
    'key': {
        'subkey': {
            'subsub': 1
        }
    }
}
flat = flatten_dict(d)
flat['key.subkey.subsub'] == 1
norm = unflatten_dict(flat)
norm['key']['subkey']['subsub'] == 1
```

"""
from typing import Any, Callable, Dict, Union
from re import compile as re_compile, Pattern, match
from ast import literal_eval
from unflatten import unflatten


def flatten_dict(
        data: Dict[str, Any],
        key_prefix: Union[str, None] = None,
        key_map: Union[Callable[[str], str], None] = str.lower) -> Dict[str, str]:
    """Flatten a dictionary to be one dimentional.

    Args:
        data (Dict[str, Any]): The dictionary to flatten.
        key_prefix (Union[str, None], optional): Key prefix to add to each key. Defaults to None.
        key_map (Union[Callable[[str], str], None], optional): A function to transform the key
                                                            strings. Defaults to str.lower.

    Raises:
        TypeError

    Returns:
        Dict[str, str]: Flat dictionary
    """
    # pylint: disable=too-many-branches
    if not isinstance(data, dict):
        if __debug__:   # pragma: no cover
            raise TypeError(
                f'data must be fo type dict, got {type(data)}')  # pragma: no cover
        raise TypeError('data must be fo type dict')
    if len(data.keys()) == 0:
        return {}
    if key_prefix is not None and not isinstance(key_prefix, str):
        raise TypeError('key_prefix must be of type str or None')
    if key_map is not None and not callable(key_map):
        raise TypeError('key_map must be callable or None')
    temp_key: Any
    for temp_key in data.keys():
        if not isinstance(temp_key, str):
            raise TypeError('all keys in data must be of type str')
    del temp_key
    out: Dict[str, str] = {}
    key: str
    for key in data.keys():
        if isinstance(data[key], dict):
            if len(data[key].keys()) == 0:
                _prefix: str = ''
                if key_prefix is not None:
                    _prefix = key_prefix + '.'
                out[_prefix + key] = str({})
            sub_prefix: str = ''
            if key_prefix is not None:
                sub_prefix = key_prefix + '.'
            sub_prefix += key
            sub: Dict[str, str] = flatten_dict(data[key], sub_prefix, key_map)
            del sub_prefix
            if len(sub.keys()) == 0:
                continue
            sub_key: str
            sub_item: str
            for sub_key, sub_item in sub.items():
                out[sub_key] = sub_item
            del sub, sub_key, sub_item
        else:
            prefix: str = ''
            if key_prefix is not None:
                prefix = key_prefix + '.'
            out[prefix + key] = str(data[key])
            del prefix
    del key
    if key_map is not None:
        return {key_map(out_key): str(out_val) for out_key, out_val in out.items()}
    return {str(out_key): str(out_val) for out_key, out_val in out.items()}
    # pylint: enable=too-many-branches


def unflatten_dict(data: Dict[str, str]) -> Dict:
    """Unflatten a flattened dictionary.

    Args:
        data (Dict[str, str]): The flat dictionary

    Raises:
        TypeError

    Returns:
        Dict: The dictionary like it was.
    """
    if not isinstance(data, dict):
        raise TypeError
    _in_data: Dict[str, str] = data.copy()
    _is_evaluable: Pattern = re_compile(
        r'^\s*(\[.*\]|\d+|\d+\.\d*|\d*\.\d+|True|False|None|\{\})\s*$')
    for _key in _in_data.keys():
        if match(_is_evaluable, _in_data[_key]) is not None:
            _in_data[_key] = literal_eval(_in_data[_key])
    _out = unflatten(_in_data)
    if isinstance(_out, dict):
        return _out
    raise TypeError  # pragma: no cover
