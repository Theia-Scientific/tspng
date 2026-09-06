#!/usr/bin/env python3

import json

from tspng.schema import coco, generic, Metadata
from typing import Any


def test_coco_json(coco_json_path):
    with open(coco_json_path) as f:
        result = coco.Json.model_validate_json(f.read())
    assert isinstance(result, coco.Json)


def test_metadata_generic_json():
    data = {"greeting": "Hello", "target": "World"}
    metadata: dict[str, dict[str, Any] | str] = {
        "data": data,
        "mime_type": generic.MIME_TYPE,
    }
    result = Metadata.model_validate(metadata)
    assert isinstance(result, Metadata)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)
    result = Metadata(data=data, mime_type=generic.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)


def test_metadata_coco_json(coco_json_path):
    with open(coco_json_path) as f:
        data = json.load(f)
    metadata: dict[str, dict[str, Any] | str] = {
        "data": data,
        "mime_type": coco.MIME_TYPE,
    }
    result = Metadata.model_validate(metadata)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
    result = Metadata(data=data, mime_type=coco.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_metadata_text():
    result = Metadata(data="Hello, World!", mime_type="text/plain")
    assert isinstance(result, Metadata)
    assert result.mime_type == "text/plain"
    assert isinstance(result.data, str)


def test_metadata_from_data_generic_json():
    data = {"greeting": "Hello", "target": "World"}
    result = Metadata.from_data(data, mime_type=None)
    assert isinstance(result, Metadata)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)


def test_metadata_from_data_coco_json(coco_json_path):
    with open(coco_json_path) as f:
        data = json.load(f)
    result = Metadata.from_data(data, mime_type=None)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_metadata_from_data_text():
    data = "Hello, World!"
    result = Metadata.from_data(data, mime_type=None)
    assert isinstance(result, Metadata)
    assert result.mime_type == "text/plain"
    assert isinstance(result.data, str)
