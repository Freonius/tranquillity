# python -m memory_profiler ./tests/profiler.py
from typing import Any, Callable, Dict, Tuple
from memory_profiler import profile
from os.path import realpath, dirname, sep
import cProfile
from ..src.shell import Shell, Capture   # TODO: Use process and capture
from re import compile, match
from json import dumps
profile_txt = realpath(dirname(__file__) + f'{sep}profiler.json')


def do_profile(func: Callable, func_args: Tuple[Any, ...], func_name: str, func_exec: str, func_setup: str = ''):
    out: Dict[str, Any] = {
        'name': func_name,
        'memory': [],
        'cProfile': [],
        'timeit': '',
        'msec': 0
    }
    _mem_capture = compile(
        r'^\s+(\d+)\s+([\d\.]+\s[MmKk]iB)?\s+([\d\.]+\s[MmKk]iB)?\s+(\d+)?\s+(.+)$')
    _prof_capture = compile(
        r'^\s+(\d+)\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)\s+(.+)$')

    with Capture() as output1:
        _e = profile(func=func)
        _e(*func_args)
        _mem_output = str(output1)
        for line in _mem_output.splitlines():
            m = match(_mem_capture, line)
            if m is not None:
                out['memory'].append({
                    'line': m.group(1),
                    'mem_usage': m.group(2),
                    'mem_increment': m.group(3),
                    'occurrences': m.group(4),
                    'content': m.group(5)
                })

    with Capture() as output2:

        cProfile.run(
            f"{func_setup};{func_exec}")
        _prof_output = str(output2)
        for line in _prof_output.splitlines():
            m = match(_prof_capture, line)
            if m is not None:
                # ncalls  tottime  percall  cumtime  percall filename:lineno(function)
                out['cProfile'].append({
                    'ncalls': m.group(1),
                    'tottime': m.group(2),
                    'percall': m.group(3),
                    'cumtime': m.group(4),
                    'percall2': m.group(5),
                    'func': m.group(6),
                })
    with Capture() as output:
        _cmd = f'''python -m timeit -s "{func_setup}" -n 500  "{func_exec}"'''
        _o = Shell.execute(_cmd)
        _ti_capture = compile(r'^\d+[^\d]+\d+:\s+(.+)\sper\sloop$')
        if tim := match(_ti_capture, _o.return_string):
            out['timeit'] = tim.group(1)
            _d, _u = tim.group(1).split(' ')
            _u = _u.lower()
            _d = float(_d)
            if _u == 'sec':
                _d *= 1000
            elif _u == 'nsec':
                _d /= 1000
            out['msec'] = _d
    return out


if __name__ == '__main__':
    j = [
        do_profile(Shell.execute, ('echo', ['hello']), 'Shell.execute',
                   "Shell.execute('echo', ['hello'])", 'from tranquillity.shell import Shell'),
        do_profile(Shell.get_docker_id, (), 'Shell.get_docker_id',
                   "Shell.get_docker_id()", 'from tranquillity.shell import Shell'),
    ]
    with open(profile_txt, 'w') as _fh:
        _fh.write(dumps(j))
    for x in j:
        print(x['msec'])
