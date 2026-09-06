#!/usr/env/bin python3

import io
import logging
import os

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from tspng.schema import Metadata, text

LOGGER: logging.Logger = logging.getLogger(__name__)


def implant(
    data: Metadata | str | os.PathLike | bytes,
    src: str | os.PathLike | io.BytesIO | Image.Image,
    dst: str | os.PathLike | io.BytesIO,
    default_mime_type: str = text.MIME_TYPE,
):
    """
    Adds data to a PNG image.

    Parameters:
        data (Metadata, str, Path): Dictionary-like object to implant in image
        src (str, path, io.BytesIO, Image.Image): The source image.
        dst (str, path, io.BytesIO): The destination image.

    Raises:
        TypeError: If data is not a path to a file or a string.
    """
    LOGGER.debug(f"{data=}")
    LOGGER.debug(f"{src=}")
    LOGGER.debug(f"{dst=}")
    if (
        isinstance(data, str)
        or isinstance(data, os.PathLike)
        or isinstance(data, bytes)
    ):
        metadata = Metadata.load(data)
    else:
        metadata = data
    png_info = PngInfo()
    if metadata.mime_type is None:
        key = default_mime_type
    else:
        key = metadata.mime_type
    LOGGER.debug(f"{key=}")
    png_info.add_text(key, metadata.text)
    LOGGER.debug(f"{png_info=}")
    if (
        isinstance(src, str)
        or isinstance(src, os.PathLike)
        or isinstance(src, io.BytesIO)
    ):
        target_im = Image.open(src)
    else:
        target_im = src
    target_im.save(dst, format="PNG", pnginfo=png_info)


def implant_into_file(
    data: Metadata | str | os.PathLike | bytes,
    src: str | os.PathLike | io.BytesIO | Image.Image,
    dst: str | os.PathLike,
    default_mime_type: str = text.MIME_TYPE,
):
    implant(data, src, dst, default_mime_type=default_mime_type)


def implant_into_bytes(
    data: Metadata | str | os.PathLike | bytes,
    src: str | os.PathLike | io.BytesIO | Image.Image,
    dst: io.BytesIO,
    default_mime_type: str = text.MIME_TYPE,
):
    implant(data, src, dst, default_mime_type=default_mime_type)
