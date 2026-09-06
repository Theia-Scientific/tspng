#!/usr/bin/env python3

from __future__ import annotations

import json

from pydantic import BaseModel, model_validator, TypeAdapter
from tspng.schema import coco, generic, text, ts
from typing import Self, TypeAlias

Data: TypeAlias = ts.Json | coco.Json | generic.Json | str


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
            elif isinstance(value, ts.Json):
                self.mime_type = ts.MIME_TYPE
            elif isinstance(value, dict):
                self.mime_type = generic.MIME_TYPE
            else:
                self.mime_type = text.MIME_TYPE
        return self

    @property
    def text(self) -> str:
        if isinstance(self.data, coco.Json):
            return self.data.model_dump_json()
        elif isinstance(self.data, ts.Json):
            return self.data.model_dump_json()
        elif isinstance(self.data, dict):
            return json.dumps(self.data)
        else:
            return self.data
