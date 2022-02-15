from typing import Type, TypeVar
from flask import request
from werkzeug.datastructures import FileStorage

T = TypeVar('T', bound='File')


class File:
    @classmethod
    def from_flask(cls: Type[T], key: str) -> T:
        if key not in request.files.keys():
            raise KeyError
        _fs: FileStorage = request.files[key]
        raise NotImplementedError

    def save_to_s3(self) -> bool:
        raise NotImplementedError

    def save_to_cloud_storage(self) -> bool:
        raise NotImplementedError

    def save(self, path: str) -> bool:
        raise NotImplementedError
