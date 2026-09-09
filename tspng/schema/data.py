#!/usr/bin/env python3

from __future__ import annotations

import errno
import io
import json
import logging
import os

from PIL.PngImagePlugin import PngInfo
from pydantic import BaseModel, model_validator, TypeAdapter
from tspng.schema import coco, generic, text, ts
from tspng.schema.ts import v1
from typing import Self, TypeAlias

LOGGER: logging.Logger = logging.getLogger(__name__)

Data: TypeAlias = v1.Json | coco.Json | generic.Json | str


class Embedded(BaseModel):
    data: Data
    mime_type: str | None = None

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

    @property
    def ext(self) -> str:
        if isinstance(self.data, coco.Json):
            return coco.FILE_EXT
        elif isinstance(self.data, v1.Json):
            return ts.FILE_EXT
        elif isinstance(self.data, dict):
            return generic.FILE_EXT
        else:
            return text.FILE_EXT

    @property
    def key(self) -> str:
        if self.mime_type is None:
            return text.MIME_TYPE
        else:
            return self.mime_type

    @staticmethod
    def load(src: os.PathLike[str] | io.StringIO) -> Embedded:
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
        return Embedded(data=data)

    @property
    def png_info(self) -> PngInfo:
        png_info = PngInfo()
        png_info.add_text(self.key, self.text)
        return png_info

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

    @model_validator(mode="after")
    def validate_mime_type(self) -> Self:
        type_adapter: TypeAdapter[Data] = TypeAdapter(Data)
        if self.mime_type is None:
            value = type_adapter.validate_python(self.data)
            if isinstance(value, coco.Json):
                self.mime_type = coco.MIME_TYPE
            elif isinstance(value, v1.Json):
                self.mime_type = ts.MIME_TYPE
            elif isinstance(value, dict):
                self.mime_type = generic.MIME_TYPE
            else:
                self.mime_type = text.MIME_TYPE
        return self


class Meta(BaseModel):
    author: str | None
    comment: str | None
    description: str | None
    copyright: str | None
    creation_time: str | None
    disclaimer: str | None
    embedded: Embedded | None
    title: str | None
    software: str | None
    source: str | None

    @property
    def png_info(self) -> PngInfo:
        png_info = PngInfo()
        if self.author is not None:
            png_info.add_text("Author", self.author)
        if self.copyright is not None:
            png_info.add_text("Copyright", self.copyright)
        if self.creation_time is not None:
            png_info.add_text("Creation Time", self.creation_time)
        if self.comment is not None:
            png_info.add_text("Comment", self.comment)
        if self.description is not None:
            png_info.add_text("Description", self.description)
        if self.disclaimer is not None:
            png_info.add_text("Disclaimer", self.disclaimer)
        if self.embedded is not None:
            png_info.add_text(self.embedded.key, self.embedded.text)
        if self.software is not None:
            png_info.add_text("Software", self.software)
        if self.source is not None:
            png_info.add_text("Source", self.source)
        if self.title is not None:
            png_info.add_text("Title", self.title)
        return png_info
