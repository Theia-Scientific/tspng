#!/usr/bin/env python3

import pytest

from io import BytesIO
from pathlib import Path
from PIL import Image
from tspng import PathDoesNotExist, PathIsNotAFile
from tspng.extraction import (
    EmbededDataNotFound,
    _open_image,
    extract,
    extract_from_bytes,
    extract_from_file,
    extract_from_files,
    extract_from_folder,
    extract_from_url,
    NotPngFormat,
    PathDoesNotContainPngs,
    PathIsNotADir,
)
from tspng.schema import Metadata
from tspng.schema.ts import v1
from urllib.error import HTTPError


@pytest.fixture
def empty_jpeg_path(tmp_path) -> Path:
    empty_jpeg_path = tmp_path.joinpath("empty.jpeg")
    image = Image.new("RGB", (640, 640))
    image.save(empty_jpeg_path, format="JPEG")
    return empty_jpeg_path


@pytest.fixture
def example_file_1_url() -> str:
    return "https://bounding-box-instructions.s3.amazonaws.com/example_file_1.ts.png"


def test_extract_with_file_path(example_file_1_path):
    result = extract(example_file_1_path)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)


def test_extract_with_file_str(example_file_1_path):
    result = extract(str(example_file_1_path))
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)


def test_extract_with_files(example_file_1_path, example_file_2_path):
    example_file_1_str = str(example_file_1_path)
    example_file_2_str = str(example_file_2_path)
    files = [
        example_file_1_path,
        example_file_2_path,
    ]
    result = extract(files)
    assert isinstance(result, dict)
    assert example_file_1_str in result
    assert isinstance(result[example_file_1_str], Metadata)
    assert result[example_file_1_str].mime_type == v1.MIME_TYPE
    assert isinstance(result[example_file_1_str].data, v1.Json)
    assert example_file_2_str in result
    assert isinstance(result[example_file_2_str], Metadata)
    assert result[example_file_1_str].mime_type == v1.MIME_TYPE
    assert isinstance(result[example_file_2_str].data, v1.Json)


def test_extract_with_folder(
    assets_directory_path, example_file_1_path, example_file_2_path
):
    example_file_1_str = str(example_file_1_path)
    example_file_2_str = str(example_file_2_path)
    result = extract(assets_directory_path)
    assert isinstance(result, dict)
    assert example_file_1_str in result
    assert isinstance(result[example_file_1_str], Metadata)
    assert result[example_file_1_str].mime_type == v1.MIME_TYPE
    assert isinstance(result[example_file_1_str].data, v1.Json)
    assert example_file_2_str in result
    assert isinstance(result[example_file_2_str], Metadata)
    assert result[example_file_1_str].mime_type == v1.MIME_TYPE
    assert isinstance(result[example_file_2_str].data, v1.Json)


def test_extract_with_url(example_file_1_url):
    result = extract(example_file_1_url)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)


def test_extract_with_bytes(example_file_1_path):
    with open(example_file_1_path, "rb") as fh:
        buf = BytesIO(fh.read())
    result = extract(buf)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)


def test_extract_fails():
    with pytest.raises(TypeError):
        extract("Test for failure")


def test_extract_from_bytes(example_file_1_path):
    with open(example_file_1_path, "rb") as fh:
        buf = BytesIO(fh.read())
    result = extract_from_bytes(buf)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)


def test_extract_from_file(example_file_1_path):
    result = extract_from_file(example_file_1_path)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)


def test_extract_from_file_not_exists_fails():
    with pytest.raises(PathDoesNotExist):
        extract_from_file(Path("Random/path.png"))


def test_extract_from_file_with_directory_fails(assets_directory_path):
    with pytest.raises(PathIsNotAFile):
        extract_from_file(assets_directory_path)


def test_extract_from_files(example_file_1_path, example_file_2_path):
    example_file_1_str = str(example_file_1_path)
    example_file_2_str = str(example_file_2_path)
    files = [
        example_file_1_path,
        example_file_2_path,
    ]
    result = extract_from_files(files)
    assert isinstance(result, dict)
    assert example_file_1_str in result
    assert isinstance(result[example_file_1_str], Metadata)
    assert result[example_file_1_str].mime_type == v1.MIME_TYPE
    assert isinstance(result[example_file_1_str].data, v1.Json)
    assert example_file_2_str in result
    assert isinstance(result[example_file_2_str], Metadata)
    assert result[example_file_1_str].mime_type == v1.MIME_TYPE
    assert isinstance(result[example_file_2_str].data, v1.Json)


def test_extract_from_folder(
    assets_directory_path, example_file_1_path, example_file_2_path
):
    example_file_1_str = str(example_file_1_path)
    example_file_2_str = str(example_file_2_path)
    result = extract_from_folder(assets_directory_path)
    assert isinstance(result, dict)
    assert example_file_1_str in result
    assert isinstance(result[example_file_1_str], Metadata)
    assert result[example_file_1_str].mime_type == v1.MIME_TYPE
    assert isinstance(result[example_file_1_str].data, v1.Json)
    assert example_file_2_str in result
    assert isinstance(result[example_file_2_str], Metadata)
    assert result[example_file_1_str].mime_type == v1.MIME_TYPE
    assert isinstance(result[example_file_2_str].data, v1.Json)


def test_extract_from_folder_fails(example_file_1_path):
    with pytest.raises(PathIsNotADir):
        extract_from_folder(example_file_1_path)


def test_extract_from_folder_fails_with_empty_files(tmp_path):
    with pytest.raises(PathDoesNotContainPngs):
        extract_from_folder(tmp_path)


def test_extract_from_url(example_file_1_url):
    result = extract_from_url(example_file_1_url)
    assert isinstance(result, Metadata)
    assert result.mime_type == v1.MIME_TYPE
    assert isinstance(result.data, v1.Json)


def test_extract_from_url_fails():
    with pytest.raises(HTTPError):
        extract_from_url(
            "https://bounding-box-instructions.s3.amazonaws.com/example_file_4.ts.png"
        )


def test_open_image_with_mime_type(example_file_1_path):
    result = _open_image(example_file_1_path, mime_type=v1.MIME_TYPE)
    assert isinstance(result, dict)


def test_open_image_not_png_fails(empty_jpeg_path):
    with pytest.raises(NotPngFormat):
        _open_image(empty_jpeg_path)


def test_open_image_fails_no_embedded_data(empty_png_path):
    with pytest.raises(EmbededDataNotFound):
        _ = _open_image(empty_png_path)
