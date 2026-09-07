import os

from importlib import metadata

__app_name__ = "tspng"
__version__ = metadata.version(__package__ or __name__)

PNG_FILE_EXT: str = ".png"


class PathDoesNotExist(Exception):
    def __init__(self, path: os.PathLike[str]):
        self.path: os.PathLike[str] = path
        super().__init__()


class PathIsNotAFile(Exception):
    def __init__(self, path: os.PathLike[str]):
        self.path: os.PathLike[str] = path
        super().__init__()
