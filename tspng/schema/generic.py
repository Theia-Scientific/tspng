#!/usr/bin/env python3

from tspng import PNG_FILE_EXT
from typing import Any, TypeAlias

FILE_EXT: str = f".json{PNG_FILE_EXT}"
MIME_TYPE: str = "application/json"

Json: TypeAlias = dict[str, Any]
