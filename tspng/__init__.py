import os

__app_name__ = "tspng"
__version__ = "1.0.0"

DEFAULT_MIME_TYPE = "application/vnd.theiascope.io+json"

MIME_TYPE = os.getenv("TSPNG_MIME_TYPE") or DEFAULT_MIME_TYPE
