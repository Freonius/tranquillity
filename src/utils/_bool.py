from typing import Union


def to_bool(val: Union[str, None, int, float]) -> bool:
    """Convert a value to a boolean.

    Args:
        val (Union[str, None, int, float]): Value to convert to bool.

    Raises:
        TypeError

    Returns:
        bool: Converted bool value
    """
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return float(val) >= 1.
    if val is None:
        return False
    if not isinstance(val, str):
        raise TypeError('Can only convert str, int, float, None, and bool')
    val = val.lower().strip()
    if val in {'t', 'true', 'yes', 'y', 'ok'}:
        return True
    if val.isdigit():
        return int(val) > 0
    return False
