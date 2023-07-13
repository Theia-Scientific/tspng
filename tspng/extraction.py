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
