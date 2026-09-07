#!/usr/bin/env python3

import logging
import sys
import typer

from pathlib import Path
from pydantic import TypeAdapter
from tspng import __app_name__, __version__, extraction as E, implantation as I
from tspng.schema import Metadata
from tspng.schema.ts import v1
from typing import Annotated

LOGGER: logging.Logger = logging.getLogger(__name__)

PREFIX: str = f"{__app_name__.upper()}"

app = typer.Typer()


def map_verbosity(count: int) -> str:
    if count == 1:
        log_level = "INFO"
    elif count >= 2:
        log_level = "DEBUG"
    else:
        log_level = "WARNING"
    return log_level


def version_callback(value: bool):
    if value:
        print(f"{__app_name__} {__version__}")
        raise typer.Exit()


@app.command()
def extract(
    inputs: Annotated[list[Path], typer.Argument(help="PNG image files.")],
):
    extractions = E.extract_from_files(inputs)
    if len(extractions) > 1:
        print(
            TypeAdapter(dict[str, Metadata])
            .dump_json(extractions, exclude_none=True)
            .decode("UTF-8")
        )
    else:
        key = list(extractions.keys())[0]
        print(extractions[key].model_dump_json(exclude_none=True))


@app.command()
def implant(
    data_file: Annotated[Path, typer.Argument(help="A data file.")],
    png_file: Annotated[Path, typer.Argument(help="A PNG image file.")],
):
    I.implant(data_file, png_file, png_file.with_suffix(v1.FILE_EXT))


@app.callback()
def main(
    verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            help="Print debugging statements to STDERR.",
            count=True,
        ),
    ] = 0,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            help="Prints the version to STDOUT",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
):
    logging.basicConfig(stream=sys.stderr, level=map_verbosity(verbose))
    LOGGER.debug(f"version={version}")
    LOGGER.debug(f"verbose={verbose}")


if __name__ == "__main__":
    app(prog_name=__app_name__)
