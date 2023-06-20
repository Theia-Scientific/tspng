#import statements
from PIL import Image

import json
import os

def extraction(path):
    #open
    abs_path=os.path.abspath(path)
    im=Image.open(abs_path)
    meta=im.text
    #load
    dict=json.loads(meta['application/vnd.theiascope.io+json'])
    return dict
