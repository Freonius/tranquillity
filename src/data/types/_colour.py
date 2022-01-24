from dataclasses import dataclass
from typing import Union
from enum import Enum, auto


class ColourType(Enum):
    RGB = auto()
    CMYK = auto()


@dataclass
class RGBA:
    red: int
    green: int
    blue: int
    alpha: Union[int, None] = None


@dataclass
class CMYK:
    cyan: int
    magenta: int
    yellow: int
    black: int
