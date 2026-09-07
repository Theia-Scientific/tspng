#!/usr/bin/env python3

import json
import pytest

from tspng import PathDoesNotExist, PathIsNotAFile
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
    assert result.ext == generic.FILE_EXT
    result = Metadata(data=data, mime_type=generic.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)
    assert result.text == json.dumps(result.data)
    assert result.ext == generic.FILE_EXT
    result = Metadata(data=data)
    assert isinstance(result, Metadata)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)
    assert result.text == json.dumps(result.data)
    assert result.ext == generic.FILE_EXT


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
    assert result.ext == v1.FILE_EXT
    result = Metadata(data=data, mime_type=v1.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == v1.FILE_EXT
    result = Metadata(data=data)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == v1.FILE_EXT


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
    assert result.ext == coco.FILE_EXT
    result = Metadata(data=data, mime_type=coco.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == coco.FILE_EXT
    result = Metadata(data=data)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == coco.FILE_EXT


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
    assert result.ext == text.FILE_EXT
    result = Metadata(data=data, mime_type=text.MIME_TYPE)
    assert isinstance(result, Metadata)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
    assert result.ext == text.FILE_EXT
    result = Metadata(data=data)
    assert isinstance(result, Metadata)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
    assert result.ext == text.FILE_EXT


def test_metadata_load_fails_file_not_exists(tmp_path):
    with pytest.raises(PathDoesNotExist):
        Metadata.load(tmp_path.joinpath("random.png"))


def test_metadata_load_fails_path_not_file(tmp_path):
    with pytest.raises(PathIsNotAFile):
        Metadata.load(tmp_path)
