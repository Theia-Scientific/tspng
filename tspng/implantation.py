#!/usr/env/bin python3

import io
import logging
import os

from PIL import Image
from tspng.schema.data import Meta

LOGGER: logging.Logger = logging.getLogger(__name__)


def implant(
    data: Embedded | os.PathLike[str],
    src: os.PathLike[str] | io.BytesIO | Image.Image,
    dst: os.PathLike[str] | io.BytesIO,
):
    """
    Adds data to a PNG image.

    Parameters:
        data (Metadata, str, os.PathLike, bytes): Dictionary-like object to
            implant in an image or the path to a file to load or a bytes.
        src (str, path, io.BytesIO, Image.Image): The source image.
        dst (str, path, io.BytesIO): The destination image.
    """
    LOGGER.debug(f"{data=}")
    LOGGER.debug(f"{src=}")
    LOGGER.debug(f"{dst=}")
    if isinstance(data, os.PathLike):
        metadata = Embedded.load(data)
    else:
        metadata = data
    if (
        isinstance(src, str)
        or isinstance(src, os.PathLike)
        or isinstance(src, io.BytesIO)
    ):
        target_im = Image.open(src)
    else:
        target_im = src
    target_im.save(dst, format="PNG", pnginfo=metadata.png_info)


def implant_into_file(
    data: Embedded | os.PathLike[str],
    src: os.PathLike[str] | io.BytesIO | Image.Image,
    dst: os.PathLike[str],
):
    """
    Adds data to a PNG image file.

    Parameters:
        data (Metadata, str, os.PathLike, bytes): Dictionary-like object to
            implant in an image or the path to a file to load or a bytes.
        src (str, path, io.BytesIO, Image.Image): The source image.
        dst (str, path): The destination image.
    """
    implant(data, src, dst)


def implant_into_bytes(
    data: Embedded | os.PathLike[str],
    src: os.PathLike[str] | io.BytesIO | Image.Image,
    dst: io.BytesIO,
):
    """
    Adds data to a buffer as a PNG image.

    Parameters:
        data (Metadata, str, os.PathLike, bytes): Dictionary-like object to
            implant in an image or the path to a file to load or a bytes.
        src (str, path, io.BytesIO, Image.Image): The source image.
        dst (io.BytesIO): The buffer.
    """
    implant(data, src, dst)
