#!/usr/bin/env python3

from __future__ import annotations

import json
import logging
import os

from pydantic import BaseModel, model_validator, TypeAdapter
from tspng import PathDoesNotExist, PathIsNotAFile
from tspng.schema import coco, generic, text
from tspng.schema.ts import v1
from typing import Self, TypeAlias

LOGGER: logging.Logger = logging.getLogger(__name__)

Data: TypeAlias = v1.Json | coco.Json | generic.Json | str

KNOWN_MIME_TYPES = [v1.MIME_TYPE, coco.MIME_TYPE, generic.MIME_TYPE, text.MIME_TYPE]


class Metadata(BaseModel):
    data: Data
    mime_type: str | None = None

    @model_validator(mode="after")
    def validate_mime_type(self) -> Self:
        type_adapter = TypeAdapter(Data)
        if self.mime_type is None:
            value = type_adapter.validate_python(self.data)
            if isinstance(value, coco.Json):
                self.mime_type = coco.MIME_TYPE
            elif isinstance(value, v1.Json):
                self.mime_type = v1.MIME_TYPE
            elif isinstance(value, dict):
                self.mime_type = generic.MIME_TYPE
            else:
                self.mime_type = text.MIME_TYPE
        return self

    @property
    def text(self) -> str:
        if isinstance(self.data, coco.Json):
            return self.data.model_dump_json()
        elif isinstance(self.data, v1.Json):
            return self.data.model_dump_json()
        elif isinstance(self.data, dict):
            return json.dumps(self.data)
        else:
            return self.data

    @property
    def ext(self) -> str:
        if isinstance(self.data, coco.Json):
            return coco.FILE_EXT
        elif isinstance(self.data, v1.Json):
            return v1.FILE_EXT
        elif isinstance(self.data, dict):
            return generic.FILE_EXT
        else:
            return text.FILE_EXT

    @staticmethod
    def load(path: str | os.PathLike) -> Metadata:
        if not os.path.exists(path):
            LOGGER.warning(f"The '{path}' does not exist.")
            raise PathDoesNotExist(path)
        if not os.path.isfile(path):
            LOGGER.warning(f"The '{path}' is not a file.")
            raise PathIsNotAFile(path)
        text = open(path, "r").read()
        try:
            data = json.loads(text)
        except ValueError:
            data = str(text)
        return Metadata(data=data)
