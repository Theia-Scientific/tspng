#!/usr/bin/env python3

from __future__ import annotations

from pydantic import BaseModel
from typing import Any, Literal


class Annotation(BaseModel):
    created: str
    confidence: float
    database_id: int
    height: tuple[float, int]
    label: Class
    ignore: bool = False
    index: int | None = None
    segmentation: list[list[int | float]]
    tracking_id: int | None = None
    uuid: str
    width: tuple[float, int]


class Class(BaseModel):
    id: int
    name: str


class FieldOfView(BaseModel):
    created: str
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


class Units(BaseModel):
    abbr: str
    name: str


class ScaleBar(BaseModel):
    length: tuple[float, float, int]
    units: Units
    x: tuple[float, int]
    y: tuple[float, int]


class Json(BaseModel):
    version: Literal["2.0"]

    annotations: list[Annotation]
    field_of_view: FieldOfView
    model: Model
    scale_bar: ScaleBar
