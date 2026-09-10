#!/usr/bin/env python3

import io
import json
import pytest

from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from tspng.schema import coco, generic, text
from tspng.schema.data import Embedded, Meta as Metadata
from tspng.schema.ts import FILE_EXT as TS_FILE_EXT, MIME_TYPE as TS_MIME_TYPE, v1, v2
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


def test_ts_v2_json(ts_v2_json_path: Path):
    with open(ts_v2_json_path) as f:
        result = v2.Json.model_validate_json(f.read())
    assert isinstance(result, v2.Json)


def test_embedded_generic_json():
    data = {"greeting": "Hello", "target": "World"}
    embedded: dict[str, generic.Json | str] = {
        "data": data,
        "mime_type": generic.MIME_TYPE,
    }
    result = Embedded.model_validate(embedded)
    assert isinstance(result, Embedded)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)
    assert result.text == json.dumps(result.data)
    assert result.ext == generic.FILE_EXT
    result = Embedded(data=data, mime_type=generic.MIME_TYPE)
    assert isinstance(result, Embedded)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)
    assert result.text == json.dumps(result.data)
    assert result.ext == generic.FILE_EXT
    result = Embedded(data=data)
    assert isinstance(result, Embedded)
    assert result.mime_type == generic.MIME_TYPE
    assert isinstance(result.data, dict)
    assert result.text == json.dumps(result.data)
    assert result.ext == generic.FILE_EXT


def test_embedded_ts_v1_modern_json(ts_v1_modern_json_path: Path):
    with open(ts_v1_modern_json_path) as f:
        data = json.load(f)
    embedded: dict[str, dict[str, Any] | str] = {
        "data": data,
        "mime_type": TS_MIME_TYPE,
    }
    result = Embedded.model_validate(embedded)
    assert isinstance(result, Embedded)
    assert result.mime_type == TS_MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == TS_FILE_EXT
    result = Embedded(data=data, mime_type=TS_MIME_TYPE)
    assert isinstance(result, Embedded)
    assert result.mime_type == TS_MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == TS_FILE_EXT
    result = Embedded(data=data)
    assert isinstance(result, Embedded)
    assert result.mime_type == TS_MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == TS_FILE_EXT


def test_embedded_ts_v1_legacy_json(ts_v1_legacy_json_path: Path):
    with open(ts_v1_legacy_json_path) as f:
        data = json.load(f)
    embedded: dict[str, dict[str, Any] | str] = {
        "data": data,
        "mime_type": TS_MIME_TYPE,
    }
    result = Embedded.model_validate(embedded)
    assert isinstance(result, Embedded)
    assert result.mime_type == TS_MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == TS_FILE_EXT
    result = Embedded(data=data, mime_type=TS_MIME_TYPE)
    assert isinstance(result, Embedded)
    assert result.mime_type == TS_MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == TS_FILE_EXT
    result = Embedded(data=data)
    assert isinstance(result, Embedded)
    assert result.mime_type == TS_MIME_TYPE
    assert isinstance(result.data, v1.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == TS_FILE_EXT


def test_embedded_coco_json(coco_json_path: Path):
    with open(coco_json_path) as f:
        data = json.load(f)
    embedded: dict[str, dict[str, Any] | str] = {
        "data": data,
        "mime_type": coco.MIME_TYPE,
    }
    result = Embedded.model_validate(embedded)
    assert isinstance(result, Embedded)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == coco.FILE_EXT
    result = Embedded(data=data, mime_type=coco.MIME_TYPE)
    assert isinstance(result, Embedded)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == coco.FILE_EXT
    result = Embedded(data=data)
    assert isinstance(result, Embedded)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
    assert result.text == result.data.model_dump_json()
    assert result.ext == coco.FILE_EXT


def test_embedded_text():
    data = "Hello, World!"
    embedded: dict[str, str] = {
        "data": data,
        "mime_type": text.MIME_TYPE,
    }
    result = Embedded.model_validate(embedded)
    assert isinstance(result, Embedded)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
    assert result.ext == text.FILE_EXT
    result = Embedded(data=data, mime_type=text.MIME_TYPE)
    assert isinstance(result, Embedded)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
    assert result.ext == text.FILE_EXT
    result = Embedded(data=data)
    assert isinstance(result, Embedded)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
    assert result.ext == text.FILE_EXT


def test_embedded_load_text(txt_file_path: Path):
    result = Embedded.load(txt_file_path)
    assert isinstance(result, Embedded)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.text == result.data
    assert result.ext == text.FILE_EXT


def test_embedded_load_fails_file_not_exists(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        _ = Embedded.load(tmp_path.joinpath("random.png"))


def test_embedded_load_fails_path_not_file(tmp_path: Path):
    with pytest.raises(IsADirectoryError):
        _ = Embedded.load(tmp_path)


def test_embedded_dump_to_file(
    coco_json_path: Path,
    txt_file_path: Path,
    ts_v1_legacy_json_path: Path,
    tmp_path: Path,
):
    with open(coco_json_path) as f:
        coco_data = json.load(f)
    coco_dst = tmp_path.joinpath("coco.json")
    actual = Embedded(data=coco_data).dump(coco_dst)
    assert coco_dst.exists()
    expected = Embedded.load(coco_dst)
    assert actual == expected

    with open(ts_v1_legacy_json_path) as f:
        v1_data = json.load(f)
    v1_dst = tmp_path.joinpath("v1.json")
    actual = Embedded(data=v1_data).dump(v1_dst)
    assert v1_dst.exists()
    expected = Embedded.load(v1_dst)
    assert actual == expected

    generic_data = {"greeting": "Hello", "target": "World"}
    generic_dst = tmp_path.joinpath("generic.json")
    _ = Embedded(data=generic_data).dump(generic_dst)
    assert generic_dst.exists()
    with open(generic_dst) as f:
        assert json.load(f) == generic_data

    with open(txt_file_path) as f:
        text_data = f.read()
    text_dst = tmp_path.joinpath("text.txt")
    _ = Embedded(data=text_data).dump(text_dst)
    assert text_dst.exists()
    with open(text_dst) as f:
        assert f.read() == text_data


def test_embedded_dump_to_buffer(
    coco_json_path: Path, txt_file_path: Path, ts_v1_legacy_json_path: Path
):
    with open(coco_json_path) as f:
        coco_data = json.load(f)
    coco_dst = io.StringIO()
    actual = Embedded(data=coco_data).dump(coco_dst)
    expected = Embedded.load(coco_dst)
    assert actual == expected

    with open(ts_v1_legacy_json_path) as f:
        v1_data = json.load(f)
    v1_dst = io.StringIO()
    actual = Embedded(data=v1_data).dump(v1_dst)
    expected = Embedded.load(v1_dst)
    assert actual == expected

    generic_data = {"greeting": "Hello", "target": "World"}
    generic_dst = io.StringIO()
    _ = Embedded(data=generic_data).dump(generic_dst)
    assert json.loads(generic_dst.getvalue()) == generic_data

    with open(txt_file_path) as f:
        text_data = f.read()
    text_dst = io.StringIO()
    _ = Embedded(data=text_data).dump(text_dst)
    assert text_dst.getvalue() == text_data


def test_metadata(empty_png_path: Path):
    data = "Hello, World!"
    metadata = Metadata(
        author="Tester",
        comment="This is a comment",
        description="This is a description",
        copyright="This is something about copyright",
        creation_time="This really should be a DateTime type",
        disclaimer="I have no responsibility",
        embedded=[
            Embedded.model_validate(
                {
                    "data": data,
                    "mime_type": text.MIME_TYPE,
                }
            )
        ],
        title="This is a Title",
        software="Generated by some software",
        source="This test",
    )
    im = Image.open(empty_png_path)
    print(metadata.png_info.chunks)
    im.save(empty_png_path, format="PNG", pnginfo=metadata.png_info)
    im.close()
    saved_im = Image.open(empty_png_path)
    assert isinstance(saved_im, PngImageFile)
    meta = saved_im.text
    assert meta is not None
    keys = meta.keys()
    assert "Author" in keys
    assert "Comment" in keys
    assert "Description" in keys
    assert "Copyright" in keys
    assert "Creation Time" in keys
    assert "Disclaimer" in keys
    assert "Title" in keys
    assert "Software" in keys
    assert "Source" in keys
    assert text.MIME_TYPE in keys
