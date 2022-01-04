"""Module for capturing output.
"""
from typing import TextIO
from io import StringIO
import sys


class Capture(list):
    """Class to capture stdout output.

    Usage:

    ```python
    what_did_I_say = ''
    with Capture() as _c:
        print('You never listen!')
        what_did_I_say = str(_c)
    ```

    """
    _stdout: TextIO
    _stringio: StringIO
    _output: str

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *_):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout

    def __repr__(self) -> str:
        return ('\n'.join(self._stringio.getvalue().splitlines())).strip()
