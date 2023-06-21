#import statements
from decouple import config
from PIL import Image

import json
import os

def extract(path):
    #open
    abs_path=os.path.abspath(path)
    im=Image.open(abs_path)
    meta=im.text
    #load
    dict=json.loads(meta[config('TSPNG_MIME_TYPE')])
    return dict
