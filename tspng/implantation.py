# import statements
import os

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from tspng import MIME_TYPE
from typing import Dict


def _implant_data(file: str, image: str, mime_type: str = MIME_TYPE) -> Dict:
    # open image
    target_im = Image.open(image)
    if target_im.format != "PNG":
        raise Exception("Image is not a PNG.")
    # load metadata
    meta = open(file, "r").read()
    # implant data
    metadata = PngInfo()
    metadata.add_text(mime_type, meta)
    # save file with implanted data
    mod_file = target_im.save(file + "+" + image, format="PNG", pnginfo=metadata)
    return mod_file


def implant(file: str, image: str, mime_type: str = MIME_TYPE) -> Dict:
    """
    Returns the metadata from a TSPNG file as a dictionary.

        Parameters:
                file (str): Path to a file
                image (str): Path to a png file as a string
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing file metadata

        Raises:
                TypeError: If not a BytesIO object, file, list of files, or folder
    """
    # call appropriate function
    if type(file) == str and os.path.isfile(file):
        return implant_to_file(file, image, mime_type)
    else:
        raise TypeError(
            f"{file} is not a BytesIO object, file, list of files, or folder."
        )


def implant_to_file(path: str, image: str, mime_type: str = MIME_TYPE) -> Dict:
    """
    Returns the metadata from a TSPNG file as a dictionary.

        Parameters:
                path (str): Path to a file as a string
                image (str): Path to a png file as a string
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing file metadata

        Raises:
                Exception: If path does not exist
                Exception: If path is not a file
                Exception: If image is not a PNG
    """
    # checks if path exists
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist.")
    # check if file exists
    if not os.path.isfile(path):
        raise Exception(f"The {path} is not a file.")
    return _implant_data(path, image, mime_type)
