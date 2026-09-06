#!/usr/bin/env python3

from pydantic import BaseModel
from tspng.schema import coco, ts


class Metadata(BaseModel):
    mime_type: str
    data: coco.Json | ts.Json
