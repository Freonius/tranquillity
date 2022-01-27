def test_suppress():
    import sys
    import io
    from ..src.shell import SuppressOutput
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    a = 'silent'

    with SuppressOutput():
        print(a)

    sys.stdout = old_stdout
    assert buffer.getvalue().strip() == a
