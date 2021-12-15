# from ._shell import Shell, ShellReturn


from sys import path
from os.path import realpath, dirname, sep
path.append(realpath(dirname(__file__) +
            f'{sep}..'))
# Keep here


def test_shell():
    from ..tranquillity.shell import Shell, ShellReturn
    ret = Shell.execute('echo ditto')
    assert isinstance(ret, ShellReturn)
    assert ret.return_string == 'ditto'
    assert ret.exit_code == 0
    assert ret.return_string == Shell.execute('echo', ['ditto']).return_string
    assert Shell.execute('exit 1').exit_code == 1
    assert Shell.execute('exit 1').return_string == ''


def test_hostname():
    from ..tranquillity.shell import Shell
    assert Shell().get_docker_id() == '127.0.0.1'
