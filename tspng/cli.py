#!/usr/bin/env python3

import json
import logging
import typer

from pathlib import Path
from tspng import __app_name__, __version__, extraction as E, implantation as I
from tspng.schema.ts import v1

LOGGER: logging.Logger = logging.getLogger(__name__)

PREFIX: str = f"{__app_name__.upper()}"

app = typer.Typer()


def map_verbosity(enabled: bool) -> str:
    if enabled:
        return "DEBUG"
    else:
        return "INFO"


def version_callback(value: bool):
    if value:
        print(f"{__app_name__} {__version__}")
        raise typer.Exit()


@app.command()
def extract(inputs: list[Path] = typer.Argument(help="PNG image files.")):
    extractions = []
    for i in inputs:
        LOGGER.debug(f"i={i}")
        extractions.append(E.extract(i))
    print(json.dumps(extractions))


@app.command()
def implant(
    data_file: Path = typer.Argument(help="A data file."),
    png_file: Path = typer.Argument(help="A PNG image file."),
):
    I.implant(data_file, png_file, png_file.name + v1.FILE_EXT)


@app.callback()
def main(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Print debugging statements to STDOUT.",
        envvar=f"{PREFIX}_VERBOSE",
    ),
    version: bool | None = typer.Option(
        None,
        "--version",
        help="Prints the version to STDOUT",
        callback=version_callback,
        is_eager=True,
    ),
):
    logging.basicConfig(level=map_verbosity(verbose))
    logging.debug(f"version={version}")


if __name__ == "__main__":
    app(prog_name=__app_name__)
