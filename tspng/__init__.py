import os

from importlib import metadata

__app_name__ = "tspng"
__version__ = metadata.version(__package__ or __name__)

DEFAULT_MIME_TYPE = "application/vnd.theiascope.io+json"

MIME_TYPE = os.getenv("TSPNG_MIME_TYPE") or DEFAULT_MIME_TYPE
