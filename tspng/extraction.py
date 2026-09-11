#!/usr/env/bin python3

import errno
import io
import logging
import os
import urllib.request

from collections.abc import Sequence
from pathlib import Path
from tspng import PNG_FILE_EXT
from tspng.schema.data import Meta as Metadata
from urllib.parse import urlparse

LOGGER: logging.Logger = logging.getLogger(__name__)


class PathDoesNotContainPngs(Exception):
    def __init__(self, path: os.PathLike[str], msg: str = ""):
        self.path: os.PathLike[str] = path
        super().__init__(msg)


def extract(
    src: str | os.PathLike[str] | io.BytesIO | Sequence[os.PathLike[str]],
) -> Metadata | dict[str, Metadata]:
    """
    Returns the metadata from a TS PNG file as either a dictionary-like object
    if a single file is extracted or a dictionary with the keys as the paths to
    the files if multiple files are extracted.

    Parameters:
        src (str, Path, io.BytesIO, List[str]): The path, byte stream, files, or
            URL to a file.

    Returns:
        (Metadata, dict): A dictionary-like object or a dictionary with the keys
            as the paths to the files and the values as a dictionary-like object
            containing the metadata

    Raises:
        TypeError: If not a BytesIO object, file, list of files, or folder
    """
    if isinstance(src, io.BytesIO):
        return extract_from_bytes(src)
    elif isinstance(src, os.PathLike) and os.path.isfile(src):
        return extract_from_file(src)
    elif isinstance(src, list):
        return extract_from_files(src)
    elif isinstance(src, Path) and os.path.isdir(src):
        return extract_from_folder(Path(src))
    elif urlparse(str(src))[0] != "":
        return extract_from_url(str(src))
    else:
        msg = f"{src} is not a BytesIO object, file, list of files, or folder."
        LOGGER.error(msg)
        raise TypeError(msg)


def extract_from_bytes(buffer: io.BytesIO) -> Metadata:
    """
    Returns the metadata from a TS PNG byte stream as a dictionary-like object.

    Parameters:
        buffer (BytesIO): Path to a byte stream
        mime_type (str, None): Optional; Media type of data

    Returns:
        (Metadata): A dictionary-like object containing the metadata from the TS
            PNG file

    Raises:
        TypeError: If buffer is not BytesIO
        Exception: If image is not a PNG
    """
    return Metadata.load(buffer)


def extract_from_file(path: os.PathLike[str]) -> Metadata:
    """
    Returns the metadata from a TS PNG file as a dictionary-like object.

    Parameters:
        path (str): Path to a file as a string
        mime_type (str, None): Optional; Media type of data

    Returns:
        (Metadata): A dictionary-like object containing the TS PNG file metadata

    Raises:
        Exception: If path does not exist
        Exception: If path is not a file
        Exception: If image is not a PNG
    """
    if not os.path.exists(path):
        LOGGER.error(f"The '{path}' path does not exist.")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    if not os.path.isfile(path):
        LOGGER.error(f"The '{path}' path is not a file.")
        raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), path)
    return Metadata.load(path)


def extract_from_files(paths: Sequence[os.PathLike[str]]) -> dict[str, Metadata]:
    """
    Returns a dictionary of dictionary-like objects from a list of TS PNG file
    paths, where the keys are the paths to the files.

    Parameters:
        path (list[str]): List of file paths
        mime_type (str, None): Optional; Media type of the embedded data

    Returns:
        (dict): Dictionary containing metadata of each file
    """
    nested_dict = {}
    for path in paths:
        nested_dict[str(path)] = extract_from_file(path)
    return nested_dict


def extract_from_folder(path: os.PathLike[str]) -> dict[str, Metadata]:
    """
    Returns a dictionary of dictionary-like objects containing the metadata from
    a folder of TS PNG file paths. The keys are the file paths.

    Parameters:
        path (str): A path to a folder
        mime_type (str, None): Optional; Media type of the embedded data

    Returns:
        (Metadata): A dictionary-like object containing the metadata of each file

    Raises:
        Exception: If path is not a directory
        Exception: If path does not contain a PNG file
    """
    if not os.path.isdir(path):
        LOGGER.error(f"The '{path}' is not a directory.")
        raise NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), path)
    file_list = []
    for file in os.listdir(path):
        root_ext = os.path.splitext(file)
        if root_ext[1] == PNG_FILE_EXT:
            file_list.append(os.path.join(path, file))
    if file_list == []:
        LOGGER.error(f"The '{path}' does not contain PNG files.")
        raise PathDoesNotContainPngs(path)
    return extract_from_files(file_list)


def extract_from_url(url: str) -> Metadata:
    """
    Returns the metadata from a TS PNG URL as a TS PNG JSON object.

    Parameters:
        url (str): URL to a TS PNG file
        mime_type (str): Optional; Media type of the embedded data

    Returns:
        (Metadata): An dictionary-like object containing the file metadata

    Raises:
        Exception: If the image cannot be obtained from the URL
    """
    response = urllib.request.urlopen(url)
    img_data = response.read()
    return Metadata.load(io.BytesIO(img_data))
