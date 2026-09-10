#!/usr/bin/env python3

from __future__ import annotations

import errno
import io
import json
import logging
import os

from datetime import datetime as DateTime
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo
from pydantic import BaseModel, ConfigDict, model_validator, TypeAdapter
from tspng.schema import coco, generic, text, ts
from tspng.schema.ts import v1
from typing import Self, TypeAlias

LOGGER: logging.Logger = logging.getLogger(__name__)

Data: TypeAlias = v1.Json | coco.Json | generic.Json | str


class MetadataNotFound(Exception):
    def __init__(self, im: Image.Image, msg: str = ""):
        self.image: Image.Image = im
        super().__init__(msg)


class NotPngFormat(Exception):
    def __init__(self, im: Image.Image, msg: str = ""):
        self.image: Image.Image = im
        super().__init__(msg)


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
        LOGGER.debug(f"{src=}")
        if isinstance(src, io.StringIO):
            text = src.getvalue()
        else:
            if not os.path.exists(src):
                LOGGER.error(f"The '{src}' does not exist.")
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src)
            if not os.path.isfile(src):
                LOGGER.error(f"The '{src}' is not a file.")
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
    author: str | None = None
    comment: str | None = None
    copyright: str | None = None
    creation_time: DateTime | str | None = None
    description: str | None = None
    disclaimer: str | None = None
    embedded: list[Embedded] = []
    title: str | None = None
    software: str | None = None
    source: str | None = None

    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    @staticmethod
    def load(src: os.PathLike[str] | io.BytesIO) -> Meta:
        LOGGER.debug(f"{src=}")
        im = Image.open(src)
        if not isinstance(im, PngImageFile):
            LOGGER.error("The source is not a PNG image.")
            raise NotPngFormat(im)
        meta = im.text
        if meta is None:
            LOGGER.error("There is no metadata.")
            raise MetadataNotFound(im)
        metadata = Meta()
        for key, value in meta.items():
            LOGGER.debug(f"{key=}")
            if key in [
                ts.MIME_TYPE,
                coco.MIME_TYPE,
                generic.MIME_TYPE,
                text.MIME_TYPE,
            ]:
                metadata.embedded.append(Embedded.load(io.StringIO(value)))
            else:
                name = key.lower().replace(" ", "_")
                LOGGER.debug(f"{name=}")
                if hasattr(metadata, name):
                    setattr(metadata, name, value)
                else:
                    LOGGER.warning(f"Unrecognized key: {key}")
        return metadata

    @property
    def png_info(self) -> PngInfo:
        png_info = PngInfo()
        for name in Meta.model_fields.keys():
            value = getattr(self, name)
            if value is not None:
                if name == "embedded":
                    for embed in value:
                        png_info.add_text(embed.key, embed.text)
                elif name == "creation_time" and isinstance(
                    self.creation_time, DateTime
                ):
                    png_info.add_text(
                        name.title().replace("_", " "),
                        self.creation_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                    )
                else:
                    png_info.add_text(name.title().replace("_", " "), value)
        return png_info
