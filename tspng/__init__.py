import os

DEFAULT_TSPNG_MIME_TYPE="application/vnd.theiascope.io+json"

MIME_TYPE=os.getenv("TSPNG_MIME_TYPE") or DEFAULT_TSPNG_MIME_TYPE
