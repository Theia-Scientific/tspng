#!/usr/bin/env python3

from pathlib import Path
from pydantic import BaseModel
from tspng.schema import coco
from typing import Any


class ScaleBar(BaseModel):
    l_n: float | None = None
    length_e: float
    units_abbr: str
    units_name: str
    units_factor: float
    x_n: float | None = None
    y_n: float | None = None


class Ruler(BaseModel):
    color: str
    dimensions: list[int]
    end_x_n: float
    end_x_px: int
    end_y_n: float
    end_y_px: int
    length_e: float
    length_n: float
    length_px: int
    start_x_px: int
    start_y_px: int
    start_x_n: float
    start_y_n: float


class Image(coco.Image):
    field_of_view: list[float]
    uuid: str
    scale_bar: ScaleBar
    original_media_path: Path
    rulers: list[Ruler]


class Annotation(coco.Annotation):
    model_id: int
    score: float
    tracking_id: int


class Model(BaseModel):
    configuration: dict[str, Any]
    created: str
    family: str
    id: int
    name: str


class Json(BaseModel):
    annotations: list[Annotation]
    categories: list[coco.Category]
    images: list[Image]
    info: coco.Info
    licenses: list[coco.License]
    models: list[Model]
