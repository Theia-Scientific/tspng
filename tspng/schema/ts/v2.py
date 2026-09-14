#!/usr/bin/env python3

from __future__ import annotations

from pydantic import BaseModel
from typing import Any, Literal


class Annotation(BaseModel):
    confidence: float
    database_id: int
    height: Value
    label: Class
    ignore: bool = False
    index: int | None = None
    segmentation: list[tuple[int | float, int | float]]
    tracking_id: int | None = None
    uuid: str
    width: Value
    x: Value
    y: Value


class Class(BaseModel):
    id: int
    name: str


class FieldOfView(BaseModel):
    height: Value
    width: Value
    x: Value
    y: Value


class Image(BaseModel):
    original: Original
    uuid: str


class Media(BaseModel):
    name: str
    path: str


class Model(BaseModel):
    created: str
    description: str
    family: str
    id: int
    parameters: dict[str, Any]
    title: str
    uuid: str
    variant: str


class Original(BaseModel):
    dimensions: tuple[int, int]
    media: Media


class Point(BaseModel):
    x: Value
    y: Value


class Ruler(BaseModel):
    begin: Point
    color: str
    end: Point
    length: Value


class ScaleBar(BaseModel):
    length: Value
    x: Value
    y: Value


class Units(BaseModel):
    abbr: str = "px"
    e_to_px: float = 1.0
    name: str = "pixel"


class Value(BaseModel):
    e: float
    n: float
    px: int


class Json(BaseModel):
    version: Literal["2.0"]

    annotations: list[Annotation]
    field_of_view: FieldOfView
    model: Model
    rulers: list[Ruler] = []
    scale_bar: ScaleBar
    units: Units
