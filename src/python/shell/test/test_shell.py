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
    from re import match
    assert match(r'^\d+\.\d+\.\d+\.\d+$', Shell().get_docker_id()) is not None
