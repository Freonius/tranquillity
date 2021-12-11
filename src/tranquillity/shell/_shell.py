from typing import Any, Iterable, Union
from dataclasses import dataclass
from socket import gethostname, gethostbyname
from subprocess import Popen, PIPE, STDOUT
from binascii import unhexlify
from shlex import quote, join

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
        if params is not None:
            cmd = cmd.strip() + ' ' + join(list(map(quote, list(map(str, params)))))
        _proc: Popen[bytes] = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        _stdout_b: bytes
        _stderr_b: bytes 
        _stdout_b, _stderr_b = _proc.communicate()
        _ret_code: int = _proc.returncode
        _stdout: str = _stdout_b.decode('utf-8').strip()
        del _stdout_b
        _stderr: str = _stderr_b.decode('utf-8').strip()
        del _stderr_b
        return ShellReturn(_ret_code, _stdout, _stderr)

    @staticmethod
    def get_docker_id() -> str:
        host_ip: str = gethostbyname(gethostname())
        cmd: str = 'echo $(basename $(cat /proc/1/cpuset))'
        try:
            container_id: str = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True).communicate()[
                0].decode('utf-8').strip()[:12]
            unhexlify(container_id)
            return container_id
        except Exception:
            return host_ip
