# -*- coding: utf-8 -*-
# pylint: enable=missing-function-docstring,missing-module-docstring,missing-class-docstring
"""Module for shell utilities.

"""
from typing import Any, Iterable, Union
from dataclasses import dataclass
from socket import gethostname, gethostbyname
from subprocess import Popen, PIPE, STDOUT
from binascii import unhexlify, Error
from shlex import quote, join


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
        _host_ip: str = gethostbyname(gethostname())
        _cmd: str = 'echo $(basename $(cat /proc/1/cpuset))'
        try:
            _proc: Popen
            with Popen(_cmd, stdout=PIPE, stderr=STDOUT, shell=True) as _proc:
                _container_id: str = _proc.communicate()[
                    0].decode('utf-8').strip()[:12]
                unhexlify(_container_id)
                return _container_id  # pragma: no cover
        except Error:
            return _host_ip
