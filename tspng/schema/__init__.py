#!/usr/bin/env python3

from __future__ import annotations

import errno
import io
import json
import logging
import os

from pydantic import BaseModel, model_validator, TypeAdapter
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
        type_adapter: TypeAdapter[Data] = TypeAdapter(Data)
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
    def load(src: os.PathLike[str] | io.StringIO) -> Metadata:
        if isinstance(src, io.StringIO):
            text = src.getvalue()
        else:
            if not os.path.exists(src):
                LOGGER.warning(f"The '{src}' does not exist.")
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src)
            if not os.path.isfile(src):
                LOGGER.warning(f"The '{src}' is not a file.")
                raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), src)
            text = open(src, "r").read()
        try:
            data = json.loads(text)
        except ValueError:
            data = str(text)
        return Metadata(data=data)

    def dump(
        self,
        dst: os.PathLike[str] | io.StringIO,
        encoding: str = "utf8",
        indent: int = 2,
    ) -> Self:
        LOGGER.debug(f"{dst=}")
        LOGGER.debug(f"{encoding=}")
        LOGGER.debug(f"{indent=}")
        if isinstance(dst, io.StringIO):
            fp = dst
        else:
            fp = open(dst, "w")
        if isinstance(self.data, coco.Json) or isinstance(self.data, v1.Json):
            fp.write(self.data.model_dump_json(indent=indent, exclude_none=True))
        elif isinstance(self.data, dict):
            generic_json_type = TypeAdapter(generic.Json)
            fp.write(
                generic_json_type.dump_json(
                    self.data, indent=indent, exclude_none=True
                ).decode("utf8")
            )
        else:
            fp.write(self.data)
        if not isinstance(dst, io.StringIO):
            fp.close()
        return self
