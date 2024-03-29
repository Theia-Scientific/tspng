# import statements
import os
import json

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from tspng import MIME_TYPE


def _implant_data(data: str, image: str, mime_type: str = MIME_TYPE):
    # open image
    target_im = Image.open(image)
    # implant data
    metadata = PngInfo()
    metadata.add_text(mime_type, data)
    # save file with implanted data
    base, _ = os.path.splitext(image)
    target_im.save(base + ".ts.png", format="PNG", pnginfo=metadata)


def implant(data: str, image: str, mime_type: str = MIME_TYPE):
    """
    Adds data to a PNG image.

        Parameters:
                data (str): Path to a file
                image (str): Path to a png file as a string
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Raises:
                TypeError: If not a BytesIO object, file, list of files, or folder
    """
    # call appropriate function
    if type(data) == str and os.path.isfile(data):
        implant_into_file(data, image, mime_type)
    else:
        raise TypeError(f"{data} is not a file.")


def implant_into_file(path: str, image: str, mime_type: str = MIME_TYPE):
    """
    Adds data to a PNG image file.

        Parameters:
                path (str): Path to a file as a string
                image (str): Path to a png file as a string
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

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
    # open file
    data = open(path, "r").read()
    # check if data is JSON string
    if json.loads(data):
        # pass JSON string to _implant_data
        _implant_data(data, image, mime_type)
    else:
        raise TypeError(f"{data} is not a JSON string.")
