#!/usr/bin/env python3

from __future__ import annotations

import json

from pydantic import BaseModel
from tspng.schema import coco, ts
from typing import Any
from typing_extensions import TypeAlias

Json: TypeAlias = dict[str, Any]


class Metadata(BaseModel):
    data: coco.Json | ts.Json | Json
    mime_type: str

    @staticmethod
    def from_json(image: Json, mime_type: str) -> Metadata:
        MIME_TYPE_MAP = {
            coco.MIME_TYPE: coco.Json.model_validate,
            ts.MIME_TYPE: ts.Json.model_validate,
        }
        validator = MIME_TYPE_MAP.get(mime_type)
        if validator is None:
            data = image
        else:
            data = validator(image)
        return Metadata(data=data, mime_type=mime_type)

    @property
    def text(self) -> str:
        if isinstance(self.data, coco.Json):
            return self.data.model_dump_json()
        elif isinstance(self.data, ts.Json):
            return self.data.model_dump_json()
        else:
            return json.dumps(self.data)
