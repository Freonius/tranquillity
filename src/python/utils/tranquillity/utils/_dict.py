from typing import Any, Callable, Dict, Union


def flatten_dict(
        data: Dict[str, Any],
        key_prefix: Union[str, None] = None,
        key_map: Union[Callable[[str], str], None] = str.lower) -> Dict[str, str]:
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
                continue
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
            out[(prefix + key).lower()] = str(data[key])
            del prefix
    del key
    if key_map is not None:
        return {key_map(out_key): out_val for out_key, out_val in out.items()}
    return out
    # pylint: enable=too-many-branches
