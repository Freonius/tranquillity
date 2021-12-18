from sys import path
from os.path import realpath, dirname, sep
path.append(realpath(dirname(__file__) +
            f'{sep}..'))


def test_shell():
    import sys
    import io
    from ..tranquillity.shell import SuppressOutput
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    a = 'silent'

    with SuppressOutput():
        print(a)

    sys.stdout = old_stdout
    assert buffer.getvalue().strip() == a
