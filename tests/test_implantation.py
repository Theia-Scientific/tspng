#!/usr/bin/env python3

import io

from tspng.implantation import implant, implant_into_bytes, implant_into_file
from tspng.extraction import extract
from tspng.schema import coco, Metadata


def test_implant_with_metadata(coco_json_path, empty_png_path, tmp_path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant(Metadata.load(coco_json_path), empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_implant_with_path_data(coco_json_path, empty_png_path, tmp_path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant(coco_json_path, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_implant_with_str_data(coco_json_path, empty_png_path, tmp_path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant(str(coco_json_path), str(empty_png_path), dst)
    result = extract(dst)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_implant_into_bytes(coco_json_path, empty_png_path):
    dst = io.BytesIO()
    implant_into_bytes(coco_json_path, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)


def test_implant_into_file(coco_json_path, empty_png_path, tmp_path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant_into_file(coco_json_path, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Metadata)
    assert result.mime_type == coco.MIME_TYPE
    assert isinstance(result.data, coco.Json)
