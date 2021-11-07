from typing import Any, Iterable, Tuple, Union
from dataclasses import dataclass


@dataclass
class ShellReturn:
    exit_code: int
    return_string: str
    stderr: str


class Shell:
    def __init__(self) -> None:
        pass

    @staticmethod
    def execute(cmd: str, params: Union[None, Iterable[Any]] = None) -> ShellReturn:
        raise NotImplementedError()
