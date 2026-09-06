#!/usr/bin/env python3

from __future__ import annotations

import json

from pydantic import BaseModel, TypeAdapter
from tspng.schema import coco, generic, ts

KnownJson = coco.Json | ts.Json
JsonData = KnownJson | generic.Json


class Metadata(BaseModel):
    data: JsonData | str
    mime_type: str

    @staticmethod
    def from_json(json_data: generic.Json, mime_type: str | None) -> Metadata:
        type_adapter = TypeAdapter(JsonData)
        if mime_type is None:
            data = type_adapter.validate_python(json_data)
            if isinstance(data, coco.Json):
                return Metadata(data=data, mime_type=coco.MIME_TYPE)
            elif isinstance(data, ts.Json):
                return Metadata(data=data, mime_type=ts.MIME_TYPE)
            else:
                return Metadata(data=data, mime_type=generic.MIME_TYPE)
        else:
            return Metadata(
                data=type_adapter.validate_python(json_data), mime_type=mime_type
            )

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
