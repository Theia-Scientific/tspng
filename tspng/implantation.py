# import statements
import os
import json

from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from tspng import MIME_TYPE
from typing import Union


def is_json(data: str) -> bool:
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def _implant_data(
    data: str, image: Union[str, Path], mime_type: str = MIME_TYPE, ext: str = ".ts.png"
):
    # open image
    target_im = Image.open(image)
    # implant data
    metadata = PngInfo()
    metadata.add_text(mime_type, data)
    # save file with implanted data
    base, _ = os.path.splitext(image)
    target_im.save(base + ext, format="PNG", pnginfo=metadata)


def implant(
    data: Union[str, Path], image: Union[str, Path], mime_type: str = MIME_TYPE
):
    """
    Adds data to a PNG image.

        Parameters:
                data (str, Path): Path to a file or text
                image (str, path): Path to a PNG file
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Raises:
                TypeError: If data is not a path to a file or a string.
    """
    if isinstance(data, Path) and os.path.isfile(data):
        implant_into_file(data, image, mime_type)
    elif isinstance(data, str) and os.path.isfile(data):
        implant_into_file(data, image, mime_type)
    elif isinstance(data, str) and is_json(data):
        _implant_data(data, image, mime_type)
    else:
        raise TypeError("The data is not a JSON file or string.")


def implant_into_file(
    path: Union[str, Path], image: Union[str, Path], mime_type: str = MIME_TYPE
):
    """
    Adds data to a PNG image file.

        Parameters:
                path (str): Path to a text or JSON file
                image (str): Path to a PNG file
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Raises:
                Exception: If path does not exist
                Exception: If path is not a file
                Exception: If image is not a PNG
    """
    # checks if path exists
    if not os.path.exists(path):
        raise Exception(f"The '{path}' path does not exist.")
    # check if file exists
    if not os.path.isfile(path):
        raise Exception(f"The '{path}' path is not a file.")
    # open file
    data = open(path, "r").read()
    # check if data is JSON string
    if is_json(data):
        # pass JSON string to _implant_data
        _implant_data(data, image, mime_type)
    else:
        raise TypeError("The data is not a JSON string.")
