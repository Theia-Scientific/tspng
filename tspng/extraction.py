#import statements
from PIL import Image
from tspng import MIME_TYPE

import json
import os

def extract_from_file(path, mime_type=MIME_TYPE):
    #open
    abs_path=os.path.abspath(path)
    im=Image.open(abs_path)
    meta=im.text
    #load
    dict=json.loads(meta[mime_type])
    return dict

def extract_from_files(paths, mime_type=MIME_TYPE):
    nested_dict = {}
    for path in paths:
        #open
        abs_path=os.path.abspath(path)
        im=Image.open(abs_path)
        meta=im.text
        #load
        dict=json.loads(meta[mime_type])
        #add to nested dictionary
        nested_dict[path]=dict
    return nested_dict
