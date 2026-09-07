#!/usr/bin/env python3

import io

from PIL import Image
from tspng.implantation import implant, implant_into_bytes, implant_into_file
from tspng.extraction import extract
from tspng.schema import coco, Metadata, text


def test_implant_with_unknown_mime_type(empty_png_path, txt_file_path, tmp_path):
    with open(txt_file_path, "r") as fp:
        data = str(fp.read())
    dst = tmp_path.joinpath(empty_png_path.with_suffix(text.FILE_EXT).name)
    md = Metadata(data=data, mime_type=None)
    md.mime_type = None
    assert md.mime_type is None
    implant(md, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Metadata)
    assert result.mime_type == text.MIME_TYPE
    assert isinstance(result.data, str)
    assert result.data == data


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


def test_implant_with_src_image(coco_json_path, empty_png_path, tmp_path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    src = Image.open(empty_png_path)
    implant(str(coco_json_path), src, dst)
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
