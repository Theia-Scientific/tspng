#!/usr/bin/env python3

import json

from tspng.schema import coco, generic, Metadata, text
from tspng.schema.ts import v1
from typing import Any


def test_coco_json(coco_json_path):
    with open(coco_json_path) as f:
        result = coco.Json.model_validate_json(f.read())
    assert isinstance(result, coco.Json)


def test_ts_v1_json(ts_v1_json_path):
    with open(ts_v1_json_path) as f:
        result = v1.Json.model_validate_json(f.read())
    assert isinstance(result, v1.Json)


def test_metadata_generic_json():
    data = {"greeting": "Hello", "target": "World"}
    metadata: dict[str, generic.Json | str] = {
        "data": data,
        "mime_type": generic.MIME_TYPE,
    }
    result = Metadata.model_validate(metadata)
    assert isinstance(result, Metadata)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)
    assert result.text == json.dumps(result.data)
    result = Metadata(data=data, mime_type=generic.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)
    assert result.text == json.dumps(result.data)
    result = Metadata(data=data)
    assert isinstance(result, Metadata)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)
    assert result.text == json.dumps(result.data)


def test_metadata_ts_v1_json(ts_v1_json_path):
    with open(ts_v1_json_path) as f:
        data = json.load(f)
    metadata: dict[str, dict[str, Any] | str] = {
        "data": data,
        "mime_type": v1.MIME_TYPE,
    }
    result = Metadata.model_validate(metadata)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    result = Metadata(data=data, mime_type=v1.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    result = Metadata(data=data)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()


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
    assert result.text == result.data.model_dump_json()
    result = Metadata(data=data, mime_type=coco.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
    assert result.text == result.data.model_dump_json()
    result = Metadata(data=data)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
    assert result.text == result.data.model_dump_json()


def test_metadata_text():
    data = "Hello, World!"
    metadata: dict[str, str] = {
        "data": data,
        "mime_type": text.MIME_TYPE,
    }
    result = Metadata.model_validate(metadata)
    assert isinstance(result, Metadata)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
    result = Metadata(data=data, mime_type=text.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
    result = Metadata(data=data)
    assert isinstance(result, Metadata)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
