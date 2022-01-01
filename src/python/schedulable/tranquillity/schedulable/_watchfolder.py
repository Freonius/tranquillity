from os import makedirs
from os.path import isdir
from posixpath import abspath
from time import sleep
from typing import Callable, Any, Dict, List, Union
from enum import Enum, auto
from functools import partial
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import DirCreatedEvent, DirDeletedEvent, DirModifiedEvent, DirMovedEvent, FileDeletedEvent,\
    FileModifiedEvent, FileMovedEvent, FileSystemEventHandler, FileCreatedEvent


class EventType(Enum):
    CREATED = auto()
    MODIFIED = auto()
    DELETED = auto()
    MOVED = auto()


class WatchFolder:
    _fld: str
    _sleep: float = 1.
    _action: Dict[str, Callable[[EventType, str], Any]] = {}
    _observer: Observer
    _filter: List[EventType]

    def __init__(self, path: str,
                 action: Union[Callable[[EventType, str], Any], None] = None,
                 filter: Union[List[EventType], None] = None) -> None:
        self._observer = Observer()
        self._fld = path
        if not isdir(path):
            makedirs(path, exist_ok=True)
        if action is None:
            self._action['action'] = lambda x, y: (x, y)
        else:
            self._action['action'] = action
        if filter is None:
            self._filter = [
                EventType.CREATED,
                EventType.DELETED,
                EventType.MODIFIED,
                EventType.MOVED,
            ]
        else:
            self._filter = filter

    def wrap(self, func: Callable[[EventType, str], Any]):
        self._action['action'] = func
        self.run()

    def _run(self) -> None:
        event_handler = Handler(self._action['action'], self._filter)
        self._observer.schedule(event_handler, self._fld, recursive=True)
        self._observer.start()
        try:
            while True:
                sleep(self._sleep)
                if not self._observer.is_alive:
                    break
        except Exception:
            self._observer.stop()
            raise
        self._observer.join()

    def run(self):
        t = Thread(target=self._run)
        t.daemon = True
        t.start()

    def run_blocking(self) -> None:
        self._run()


class Handler(FileSystemEventHandler):
    _action: Dict[str, Callable[[EventType, str], Any]] = {}
    _filter: List[EventType]

    def __init__(self, action: Callable[[EventType, str], Any], filter: Union[List[EventType], None] = None) -> None:
        super().__init__()
        self._action['action'] = action
        if filter is None:
            self._filter = [
                EventType.CREATED,
                EventType.DELETED,
                EventType.MODIFIED,
                EventType.MOVED,
            ]
        else:
            self._filter = filter

    def on_any_event(self, event: Union[
            FileCreatedEvent,
            FileModifiedEvent,
            FileDeletedEvent,
            DirModifiedEvent,
            FileMovedEvent,
            DirCreatedEvent,
            DirDeletedEvent,
            DirMovedEvent]):
        _action: Callable[[EventType, str], Any] = self._action['action']
        _ev_type: EventType
        if event.event_type == 'created':
            _ev_type = EventType.CREATED
        elif event.event_type == 'modified':
            _ev_type = EventType.MODIFIED
        elif event.event_type == 'moved':
            _ev_type = EventType.MOVED
        else:
            _ev_type = EventType.DELETED
        if _ev_type in self._filter:
            _action(_ev_type, abspath(event.src_path))


def watchfolder(func: Union[Callable[[EventType, str], Any], None] = None, *, path: str = '.', filter: Union[EventType, str, List[EventType], List[str], None] = None, **options: Any):
    if func is None:
        p: partial = partial(watchfolder, path=path, filter=filter, **options)
        return p

    def _ev(e: str) -> EventType:
        e = e.upper().strip()
        if e == 'CREATED':
            return EventType.CREATED
        if e == 'MODIFIED':
            return EventType.MODIFIED
        if e == 'MOVED':
            return EventType.MOVED
        return EventType.DELETED

    if isinstance(filter, EventType):
        filter = [filter]
    elif isinstance(filter, str):
        filter = [_ev(filter)]
    elif isinstance(filter, list):
        _new_filter: List[EventType] = []
        for _e in filter:
            if isinstance(_e, EventType):
                _new_filter.append(_e)
            else:
                _new_filter.append(_ev(_e))
        filter = _new_filter
        filter = list(set(filter))

    watcher: WatchFolder = WatchFolder(path, func, filter)
    watcher.run()
