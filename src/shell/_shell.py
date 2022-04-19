# -*- coding: utf-8 -*-
# pylint: enable=missing-function-docstring,missing-module-docstring,missing-class-docstring
"""Module for shell utilities.

"""
from typing import Any, Dict, Iterable, Union
from dataclasses import dataclass
from socket import gethostname, gethostbyname
from subprocess import Popen, PIPE, STDOUT
from binascii import unhexlify, Error
from shlex import quote, join
from socket import error
from paramiko import SSHClient, BadHostKeyException, AuthenticationException, SSHException
from paramiko.channel import ChannelStderrFile, ChannelFile
from ..exceptions import SSHException as _SSHException


@dataclass
class ShellReturn:
    """ Dataclass that holds all output
    from a shell command.
    """
    exit_code: int
    return_string: str
    stderr: str


class Shell:
    """ Class that holds static methods for shell
    utilities.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def execute(cmd: str, params: Union[None, Iterable[Any]] = None) -> ShellReturn:
        """Execute a shell command.

        Example:

        ```python
        from tranquillity.shell import Shell

        out = Shell.execute('echo', ['hi'])
        # Can also be Shell.execute('echo hi')
        print(out.return_string)    # hi
        print(out.exit_code)        # 0 (hopefully)
        ```

        Args:
            cmd (str): Command to execute.
            params (Union[None, Iterable[Any]], optional): Additional arguments can
                                                           be added here. Defaults to None.

        Returns:
            ShellReturn: It will have the output in str format, the error output, and the
                         return code.
        """
        if params is not None:
            cmd = cmd.strip() + ' ' + join(list(map(quote, list(map(str, params)))))
        _proc: Popen[bytes]
        with Popen(
                cmd, stdout=PIPE, stderr=STDOUT, shell=True) as _proc:
            _stdout_b: bytes
            _stderr_b: bytes
            _stdout_b, _stderr_b = _proc.communicate()
            _ret_code: int = _proc.returncode
            _stdout: str = ''
            try:
                _stdout = _stdout_b.decode('utf-8').strip()
            except AttributeError:  # pragma: no cover
                pass                # pragma: no cover
            del _stdout_b
            _stderr: str = ''
            try:
                _stderr = _stderr_b.decode('utf-8').strip()
            except AttributeError:
                pass
            del _stderr_b
            return ShellReturn(_ret_code, _stdout, _stderr)

    @staticmethod
    def get_docker_id() -> str:
        """Get the first 12 characters of a docker id, or the ip address of the host.

        Returns:
            str: docker id or ip address.
        """
        try:
            _proc: Popen
            with Popen('echo $(basename $(cat /proc/1/cpuset))',
                       stdout=PIPE, stderr=STDOUT, shell=True) as _proc:
                _container_id: str = _proc.communicate()[
                    0].decode('utf-8').strip()[:12]
                unhexlify(_container_id)
                return _container_id  # pragma: no cover
        except Error:
            return gethostbyname(gethostname())

    @staticmethod
    def ssh(host: str, cmd: str, *,
            key: Union[str, None] = None,
            port: int = 22,
            passphrase: Union[str, None] = None,
            username: Union[str, None] = None,
            password: Union[str, None] = None,
            env: Union[Dict[str, str], None] = None) -> ShellReturn:
        """_summary_

        Args:
            host (str): _description_
            cmd (str): _description_
            key (Union[str, None], optional): _description_. Defaults to None.
            port (int, optional): _description_. Defaults to 22.
            passphrase (Union[str, None], optional): _description_. Defaults to None.
            username (Union[str, None], optional): _description_. Defaults to None.
            password (Union[str, None], optional): _description_. Defaults to None.
            env (Union[Dict[str, str], None], optional): _description_. Defaults to None.

        Raises:
            _SSHException: _description_

        Returns:
            ShellReturn: _description_
        """
        _ssh: SSHClient = SSHClient()
        try:
            _ssh.connect(host,
                         port=port,
                         username=username,
                         password=password,
                         passphrase=passphrase,
                         key_filename=key)
            _stdout_channel: ChannelFile
            _stderr_channel: ChannelStderrFile
            _, _stdout_channel, _stderr_channel = _ssh.exec_command(
                cmd, environment=env)
            _stdout: str = ''.join(_stdout_channel.readlines())
            _stderr: str = ''.join(_stderr_channel.readlines())
            _ssh.close()
            return ShellReturn(0, return_string=_stdout, stderr=_stderr)
        except (error, BadHostKeyException, AuthenticationException, SSHException) as e:
            raise _SSHException('Operation not completed') from e
