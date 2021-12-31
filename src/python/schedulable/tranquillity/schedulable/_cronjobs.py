from typing import Callable
# from croniter import croniter
from datetime import datetime, time
from time import sleep


def wait_start(run_time: str, action: Callable):
    start_time: time = time(*(map(int, run_time.split(':'))))
    while start_time > datetime.today().time():
        sleep(1)
    return action
