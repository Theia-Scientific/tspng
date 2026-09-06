#!/usr/bin/env python3

from __future__ import annotations

from pydantic import BaseModel, Field, TypeAdapter
from tspng.schema import coco, generic, text, ts
from typing import Annotated, TypeAlias

Data: TypeAlias = ts.Json | coco.Json | generic.Json | str


class Metadata(BaseModel):
    data: Data
    mime_type: str

    @staticmethod
    def from_data(data: Data, mime_type: str | None) -> Metadata:
        type_adapter = TypeAdapter(Annotated[Data, Field(union_mode="left_to_right")])
        if mime_type is None:
            value = type_adapter.validate_python(data)
            if isinstance(value, coco.Json):
                return Metadata(data=value, mime_type=coco.MIME_TYPE)
            elif isinstance(value, ts.Json):
                return Metadata(data=value, mime_type=ts.MIME_TYPE)
            elif isinstance(value, dict):
                return Metadata(data=value, mime_type=generic.MIME_TYPE)
            else:
                return Metadata(data=value, mime_type=text.MIME_TYPE)
        else:
            return Metadata(
                data=type_adapter.validate_python(data), mime_type=mime_type
            )
