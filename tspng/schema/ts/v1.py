#!/usr/bin/env python3

from pydantic import BaseModel
from tspng import PNG_FILE_EXT
from tspng.schema import coco
from typing import Any

FILE_EXT: str = f".ts{PNG_FILE_EXT}"
MIME_TYPE: str = "application/vnd.theiascope.io+json"


class ScaleBar(BaseModel):
    dimensions: list[int]
    l_n: float | None = None
    length: float
    units_abbr: str
    units_name: str
    units_factor: float | None = None
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
    uuid: str | None = None
    scale_bar: ScaleBar
    original_media_path: str | None = None
    rulers: list[Ruler] | None = None


class Annotation(coco.Annotation):
    aspect_ratio: float | None = None
    bottom_most_point: list[int] | None = None
    centroid: list[int] | None = None
    equivalent_diameter: float | None = None
    extent: float | None = None
    index: int | None = None
    left_most_point: list[int] | None = None
    major_axis: float | None = None
    minor_axis: float | None = None
    model_id: int
    orientation: float | None = None
    perimeter: float | None = None
    right_most_Point: list[int] | None = None
    score: float
    top_most_point: list[int] | None = None
    tracking_id: int | None = None


class Model(BaseModel):
    configuration: dict[str, Any]
    created: str
    family: str
    id: int
    name: str
    pid: int | None = None


class Json(BaseModel):
    annotations: list[Annotation]
    categories: list[coco.Category]
    images: list[Image]
    info: coco.Info
    licenses: coco.License
    models: list[Model]
