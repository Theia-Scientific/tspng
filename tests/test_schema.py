#!/usr/bin/env python3

import io
import json
import pytest

from pathlib import Path
from tspng.schema import coco, generic, Metadata, text
from tspng.schema.ts import v1
from typing import Any


def test_coco_json(coco_json_path: Path):
    with open(coco_json_path) as f:
        result = coco.Json.model_validate_json(f.read())
    assert isinstance(result, coco.Json)


def test_ts_v1_legacy_json(ts_v1_legacy_json_path: Path):
    with open(ts_v1_legacy_json_path) as f:
        result = v1.Json.model_validate_json(f.read())
    assert isinstance(result, v1.Json)


def test_ts_v1_modern_json(ts_v1_modern_json_path: Path):
    with open(ts_v1_modern_json_path) as f:
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


def test_metadata_ts_v1_modern_json(ts_v1_modern_json_path: Path):
    with open(ts_v1_modern_json_path) as f:
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


def test_metadata_ts_v1_legacy_json(ts_v1_legacy_json_path: Path):
    with open(ts_v1_legacy_json_path) as f:
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


def test_metadata_coco_json(coco_json_path: Path):
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


def test_metadata_load_text(txt_file_path: Path):
    result = Metadata.load(txt_file_path)
    assert isinstance(result, Metadata)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
    assert result.ext == text.FILE_EXT


def test_metadata_load_fails_file_not_exists(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        _ = Metadata.load(tmp_path.joinpath("random.png"))


def test_metadata_load_fails_path_not_file(tmp_path: Path):
    with pytest.raises(IsADirectoryError):
        _ = Metadata.load(tmp_path)


def test_metadata_dump_to_file(
    coco_json_path: Path,
    txt_file_path: Path,
    ts_v1_legacy_json_path: Path,
    tmp_path: Path,
):
    with open(coco_json_path) as f:
        coco_data = json.load(f)
    coco_dst = tmp_path.joinpath("coco.json")
    actual = Metadata(data=coco_data).dump(coco_dst)
    assert coco_dst.exists()
    expected = Metadata.load(coco_dst)
    assert actual == expected

    with open(ts_v1_legacy_json_path) as f:
        v1_data = json.load(f)
    v1_dst = tmp_path.joinpath("v1.json")
    actual = Metadata(data=v1_data).dump(v1_dst)
    assert v1_dst.exists()
    expected = Metadata.load(v1_dst)
    assert actual == expected

    generic_data = {"greeting": "Hello", "target": "World"}
    generic_dst = tmp_path.joinpath("generic.json")
    _ = Metadata(data=generic_data).dump(generic_dst)
    assert generic_dst.exists()
    with open(generic_dst) as f:
        assert json.load(f) == generic_data

    with open(txt_file_path) as f:
        text_data = f.read()
    text_dst = tmp_path.joinpath("text.txt")
    _ = Metadata(data=text_data).dump(text_dst)
    assert text_dst.exists()
    with open(text_dst) as f:
        assert f.read() == text_data


def test_metadata_dump_to_buffer(
    coco_json_path: Path, txt_file_path: Path, ts_v1_legacy_json_path: Path
):
    with open(coco_json_path) as f:
        coco_data = json.load(f)
    coco_dst = io.StringIO()
    actual = Metadata(data=coco_data).dump(coco_dst)
    expected = Metadata.load(coco_dst)
    assert actual == expected

    with open(ts_v1_legacy_json_path) as f:
        v1_data = json.load(f)
    v1_dst = io.StringIO()
    actual = Metadata(data=v1_data).dump(v1_dst)
    expected = Metadata.load(v1_dst)
    assert actual == expected

    generic_data = {"greeting": "Hello", "target": "World"}
    generic_dst = io.StringIO()
    _ = Metadata(data=generic_data).dump(generic_dst)
    assert json.loads(generic_dst.getvalue()) == generic_data

    with open(txt_file_path) as f:
        text_data = f.read()
    text_dst = io.StringIO()
    _ = Metadata(data=text_data).dump(text_dst)
    assert text_dst.getvalue() == text_data
