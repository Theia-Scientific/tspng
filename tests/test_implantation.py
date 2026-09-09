#!/usr/bin/env python3

import io

from pathlib import Path
from PIL import Image
from tspng.implantation import implant, implant_into_bytes, implant_into_file
from tspng.extraction import extract
from tspng.schema import coco, text
from tspng.schema.data import Embedded


def test_implant_with_unknown_mime_type(
    empty_png_path: Path, txt_file_path: Path, tmp_path: Path
):
    with open(txt_file_path, "r") as fp:
        data = str(fp.read())
    dst = tmp_path.joinpath(empty_png_path.with_suffix(text.FILE_EXT).name)
    md = Embedded(data=data, mime_type=None)
    md.mime_type = None
    assert md.mime_type is None
    implant(md, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Embedded)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.data == data


def test_implant_with_metadata(
    coco_json_path: Path, empty_png_path: Path, tmp_path: Path
):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant(Embedded.load(coco_json_path), empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Embedded)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_implant(coco_json_path: Path, empty_png_path: Path, tmp_path: Path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant(coco_json_path, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Embedded)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_implant_with_src_image(
    coco_json_path: Path, empty_png_path: Path, tmp_path: Path
):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    src = Image.open(empty_png_path)
    implant(coco_json_path, src, dst)
    result = extract(dst)
    assert isinstance(result, Embedded)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_implant_into_bytes(coco_json_path: Path, empty_png_path: Path):
    dst = io.BytesIO()
    implant_into_bytes(coco_json_path, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Embedded)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_implant_into_file(coco_json_path: Path, empty_png_path: Path, tmp_path: Path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant_into_file(coco_json_path, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Embedded)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
