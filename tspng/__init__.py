import os

from importlib import metadata
from pathlib import Path
from typing import Union

__app_name__ = "tspng"
__version__ = metadata.version(__package__ or __name__)

DEFAULT_MIME_TYPE = "application/vnd.theiascope.io+json"

MIME_TYPE = os.getenv("TSPNG_MIME_TYPE") or DEFAULT_MIME_TYPE

class PathDoesNotExist(Exception):
    def __init__(self, path: Union[Path, str]):
        self.path = path

class PathIsNotAFile(Exception):
    def __init__(self, path: Union[Path, str]):
        self.path = path
