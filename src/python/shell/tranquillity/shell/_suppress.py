from os import open as os_open, close as os_close, dup, dup2, devnull, O_RDWR
from typing import List, Tuple


class SuppressOutput:
    null_fds: List[int]
    save_fds: Tuple[int, int]

    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os_open(devnull, O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (dup(1), dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        dup2(self.null_fds[0], 1)
        dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        dup2(self.save_fds[0], 1)
        dup2(self.save_fds[1], 2)
        # Close the null files
        os_close(self.null_fds[0])
        os_close(self.null_fds[1])
