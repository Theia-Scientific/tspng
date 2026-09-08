#!/usr/bin/env python3

from pydantic import BaseModel
from typing import Any, Literal


class Attributes(BaseModel):
    digital_micrograph: dict[str, Any] | None = None
    imagej: dict[str, Any] | None = None


class Class(BaseModel):
    id: int
    name: str


class FieldOfView(BaseModel):
    created: str
    height_n: float = 1.0
    width_n: float = 1.0
    x_n: float = 0.0
    y_n: float = 0.0


class Image(BaseModel):
    attributes: Attributes | None = None
    created: str
    origin: str
    original_height_px: int
    original_media_filename: str | None = None
    original_media_path: str | None = None
    original_width_px: int
    uuid: str


class Annotation(BaseModel):
    created: str
    confidence: float
    database_id: int
    height_n: float
    label: Class
    ignore: bool = False
    index: int | None = None
    segmentation: list[list[int | float]]
    tracking_id: int | None = None
    uuid: str
    width_n: float
    x_n: float
    y_n: float


class Model(BaseModel):
    created: str
    description: str
    family: str
    id: int
    parameters: dict[str, Any]
    title: str
    uuid: str
    variant: str


class Units(BaseModel):
    abbr: str
    name: str


class ScaleBar(BaseModel):
    length_n: float
    length_e: float
    units: Units
    x_n: float | None = None
    y_n: float | None = None


class Json(BaseModel):
    version: Literal["2.0"]

    annotations: list[Annotation]
    field_of_view: FieldOfView
    model: Model
    scale_bar: ScaleBar
