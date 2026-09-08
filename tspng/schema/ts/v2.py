#!/usr/bin/env python3

from pydantic import BaseModel
from typing import Any, Literal


class Model(BaseModel):
    created: str
    family: str
    id: int
    parameters: dict[str, Any]
    variant: str


class Json(BaseModel):
    version: Literal["2.0"]

    model: Model
