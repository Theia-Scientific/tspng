#!/usr/bin/env python3

from __future__ import annotations

from pydantic import BaseModel
from typing import Any, Literal


class Annotation(BaseModel):
    confidence: float
    database_id: int
    height: tuple[float, int]
    label: Class
    ignore: bool = False
    index: int | None = None
    segmentation: list[tuple[int | float, int | float]]
    tracking_id: int | None = None
    uuid: str
    width: tuple[float, int]


class Class(BaseModel):
    id: int
    name: str


class FieldOfView(BaseModel):
    height: tuple[float, int]
    width: tuple[float, int]
    x: tuple[float, int]
    y: tuple[float, int]


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
    x: tuple[float, int]
    y: tuple[float, int]


class Ruler(BaseModel):
    begin: Point
    color: str
    end: Point
    length: tuple[float, float, int]
    units: Units


class ScaleBar(BaseModel):
    length: tuple[float, float, int]
    units: Units
    x: tuple[float, int]
    y: tuple[float, int]


class Units(BaseModel):
    abbr: str
    name: str


class Json(BaseModel):
    version: Literal["2.0"]

    annotations: list[Annotation]
    field_of_view: FieldOfView
    model: Model
    rulers: list[Ruler]
    scale_bar: ScaleBar
