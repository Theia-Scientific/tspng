def extraction(fname):

    #import statements
    from PIL import Image

    import json

    #open
    im=Image.open(fname)
    meta=im.text
    #load
    dict=json.loads(meta['application/vnd.theiascope.io+json'])
    return dict

extraction('20230510T192247Z.722_crimson-notebook (PML).ts.png')