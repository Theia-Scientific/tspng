#!/usr/bin/env python3

import importlib.metadata

from pathlib import Path
from pydantic import TypeAdapter
from tspng import __app_name__, PNG_FILE_EXT
from tspng.cli import app, map_verbosity
from tspng.schema.data import Meta as Metadata
from tspng.schema.ts import FILE_EXT as TS_FILE_EXT, MIME_TYPE as TS_MIME_TYPE, v1
from typer.testing import CliRunner

runner = CliRunner()


def test_map_verbosity():
    assert map_verbosity(0) == "WARNING"
    assert map_verbosity(1) == "INFO"
    assert map_verbosity(2) == "DEBUG"
    assert map_verbosity(3) == "DEBUG"


def test_app_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_app_version():
    version = importlib.metadata.version(__app_name__)
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} {version}" in result.stdout


def test_app_extract(example_file_1_path: Path):
    result = runner.invoke(app, ["extract", str(example_file_1_path)])
    assert result.exit_code == 0
    assert len(result.stdout) > 0
    metadata = Metadata.model_validate_json(result.stdout)
    assert metadata.author is not None
    assert metadata.comment is not None
    assert metadata.copyright is not None
    assert metadata.creation_time is not None
    assert metadata.description is not None
    assert metadata.title is not None
    assert metadata.software is not None
    assert metadata.source is not None
    assert len(metadata.embedded) == 1
    assert metadata.embedded[0].mime_type == TS_MIME_TYPE
    assert isinstance(metadata.embedded[0].data, v1.Json)


def test_app_extract_multiple_files(
    example_file_1_path: Path, example_file_2_path: Path
):
    example_file_1_str = str(example_file_1_path)
    example_file_2_str = str(example_file_2_path)
    result = runner.invoke(
        app, ["extract", str(example_file_1_path), str(example_file_2_path)]
    )
    assert result.exit_code == 0
    assert len(result.stdout) > 0
    files_metadata = TypeAdapter(dict[str, Metadata]).validate_json(result.stdout)
    assert len(files_metadata) > 0
    assert example_file_1_str in files_metadata
    example_file_1_result = files_metadata[example_file_1_str]
    assert example_file_1_result.author is not None
    assert example_file_1_result.comment is not None
    assert example_file_1_result.copyright is not None
    assert example_file_1_result.creation_time is not None
    assert example_file_1_result.description is not None
    assert example_file_1_result.title is not None
    assert example_file_1_result.software is not None
    assert example_file_1_result.source is not None
    assert len(example_file_1_result.embedded) == 1
    assert example_file_1_result.embedded[0].mime_type == TS_MIME_TYPE
    assert isinstance(example_file_1_result.embedded[0].data, v1.Json)
    assert example_file_2_str in files_metadata
    example_file_2_result = files_metadata[example_file_2_str]
    assert example_file_2_result.author is not None
    assert example_file_2_result.comment is not None
    assert example_file_2_result.copyright is not None
    assert example_file_2_result.creation_time is not None
    assert example_file_2_result.description is not None
    assert example_file_2_result.title is not None
    assert example_file_2_result.software is not None
    assert example_file_2_result.source is not None
    assert len(example_file_2_result.embedded) == 1
    assert example_file_2_result.embedded[0].mime_type == TS_MIME_TYPE
    assert isinstance(example_file_2_result.embedded[0].data, v1.Json)


def test_app_implant(coco_json_path: Path, empty_png_path: Path):
    expected = empty_png_path.with_suffix(TS_FILE_EXT)
    result = runner.invoke(app, ["implant", str(coco_json_path), str(empty_png_path)])
    assert result.exit_code == 0
    assert expected.exists()
    assert expected.name == empty_png_path.stem + TS_FILE_EXT
    assert expected.suffix == PNG_FILE_EXT
