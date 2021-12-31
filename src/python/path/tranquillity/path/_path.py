from os.path import realpath, sep, abspath
from inspect import FrameInfo, stack
from pathlib import Path as lPath


class Path:
    @staticmethod
    def cwd() -> str:
        frame: FrameInfo = stack()[1]
        p: str = frame[0].f_code.co_filename
        cwd: str = str(lPath(realpath(p)).parent.absolute()) + sep
        return cwd

    @staticmethod
    def absolute(path: str) -> str:
        return abspath(str(lPath(path).absolute()))
