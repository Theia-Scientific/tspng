#!/usr/bin/env python3

import pytest

from pathlib import Path
from tspng.implantation import implant, implant_into_file
from tspng.extraction import extract
from tspng.schema import coco, Metadata


@pytest.fixture
def txt_file_path(tmp_path) -> Path:
    txt_path = tmp_path.joinpath("file.txt")
    with open(txt_path, "w") as f:
        f.write("Hello World! This is NOT JSON.")
    return txt_path


def test_implant_with_path(coco_json_path, empty_png_path, tmp_path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant(coco_json_path, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Metadata)


def test_implant_with_str(coco_json_path, empty_png_path, tmp_path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant(str(coco_json_path), str(empty_png_path), dst)
    result = extract(dst)
    assert isinstance(result, Metadata)


def test_implant_into_file(coco_json_path, empty_png_path, tmp_path):
    dst = tmp_path.joinpath(empty_png_path.with_suffix(coco.FILE_EXT).name)
    implant_into_file(coco_json_path, empty_png_path, dst)
    result = extract(dst)
    assert isinstance(result, Metadata)
