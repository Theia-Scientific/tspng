#!/usr/bin/env python3

from __future__ import annotations

from pydantic import BaseModel
from typing import Any, Literal


class Annotation(BaseModel):
    confidence: float
    database_id: int
    height: Number
    label: Class
    ignore: bool = False
    index: int | None = None
    segmentation: list[tuple[int | float, int | float]]
    tracking_id: int | None = None
    uuid: str
    width: Number
    x: Number
    y: Number


class Class(BaseModel):
    id: int
    name: str


class FieldOfView(BaseModel):
    height: Number
    width: Number
    x: Number
    y: Number


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


class Number(BaseModel):
    e: float
    n: float
    px: int


class Original(BaseModel):
    dimensions: tuple[int, int]
    media: Media


class Point(BaseModel):
    x: Number
    y: Number


class Ruler(BaseModel):
    begin: Point
    color: str
    end: Point
    length: Number


class ScaleBar(BaseModel):
    length: Number
    x: Number
    y: Number


class Units(BaseModel):
    abbr: str = "px"
    e_per_px: float = 1.0
    name: str = "pixel"


class Json(BaseModel):
    version: Literal["2.0"]

    annotations: list[Annotation]
    image: Image
    field_of_view: FieldOfView
    model: Model
    rulers: list[Ruler] = []
    scale_bar: ScaleBar | None
    units: Units
