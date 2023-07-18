#import statements
import json
import os
import warnings

from PIL import Image
from tspng import MIME_TYPE
from typing import Dict, List

def extract_from_file(path: str, mime_type: str=MIME_TYPE) -> Dict:
    '''
    Returns the metadata from a TSPNG file as a dictionary.

        Parameters:
                path (str): Path to a file as a string
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                dict (dict): Dictionary containing file metadata

        Raises:
                Exception: If path does not exist
                TypeError: If file is not PNG format
    '''
    #checks if path exists
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist.")
    #check if file is PNG file
    fname = os.path.split(os.path.abspath(path))[1]
    if fname[-3:] != 'png':
        raise TypeError(f"{fname} is not a PNG file.")
    #open
    im=Image.open(path)
    meta=im.text

    #load
    if mime_type in meta.keys():
        dict=json.loads(meta[mime_type])
    else:
        #warn if file has no embedded data
        warnings.warn(f"{fname} has no embedded TS metadata.")
        dict={}
    return dict

def extract_from_files(paths: List, mime_type: str=MIME_TYPE) -> Dict:
    '''
    Returns a nested dictionary of metadata from a list of TSPNG file paths.

        Parameters:
                path (list[str]): List of file paths
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                nested_dict (dict): Dictionary containing metadata of each file
    '''
    nested_dict = {}
    for path in paths:
        nested_dict[path] = extract_from_file(path, mime_type)
    return nested_dict
