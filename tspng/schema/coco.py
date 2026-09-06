#!/usr/bin/env python3

from pydantic import BaseModel

MIME_TYPE = "application/coco+json"


class Annotation(BaseModel):
    area: int
    bbox: list[int]
    category_id: int
    id: int
    image_id: int
    iscrowd: int
    segmentation: list[list[int]] | bytes | None = None


class Category(BaseModel):
    super_category: str = "none"
    id: int
    name: str


class Image(BaseModel):
    coco_url: str | None = None
    id: int
    file_name: str
    flickr_url: str | None = None
    license: int
    height: int
    width: int
    date_captured: str


class Info(BaseModel):
    contributor: str
    date_created: str
    description: str
    url: str
    version: str
    year: int | str


class License(BaseModel):
    id: int
    name: str
    url: str


class Json(BaseModel):
    info: Info
    licenses: list[License]
    categories: list[Category]
    images: list[Image]
    annotations: list[Annotation]
