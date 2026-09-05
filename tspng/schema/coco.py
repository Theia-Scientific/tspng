#!/usr/bin/env python3

from pydantic import BaseModel


class Annotation(BaseModel):
    area: int
    bbox: list[int]
    category_id: int
    id: int
    image_id: int
    iscrowd: int
    segmentation: list[int]


class Category(BaseModel):
    super_category: str = "none"
    id: int
    name: str


class Image(BaseModel):
    id: int
    license: int
    file_name: str
    height: int
    width: int
    date_captured: str


class Info(BaseModel):
    contributor: str
    date_created: str
    description: str
    url: str
    version: str
    year: str


class License(BaseModel):
    id: int
    name: str
    url: str


class Coco(BaseModel):
    info: Info
    licenses: list[License]
    categories: list[Category]
    images: list[Image]
    annotations: list[Annotation]
