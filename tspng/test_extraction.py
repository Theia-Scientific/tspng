#!/usr/bin/env python3

from io import BytesIO
from tspng.extraction import extract_from_bytes,extract_from_file,extract_from_files

def test_extract_from_bytes():
    '''
    Tests the dictionary keys from an example TS byte stream.
    '''
    with open('tests/assets/example_file_1.ts.png', 'rb') as fh:
        buf = BytesIO(fh.read())
        test_data = extract_from_bytes(buf)
        assert list(test_data.keys())==['info','licenses','images','annotations','models','categories']

def test_extract_from_file():
    '''
    Tests the dictionary keys from an example TSPNG file path.
    '''
    test_data = extract_from_file('tests/assets/example_file_1.ts.png')
    assert list(test_data.keys())==['info','licenses','images','annotations','models','categories']

def test_extract_from_files():
    '''
    Tests the dictionary keys from a list of example TSPNG file paths.
    '''
    test_data = extract_from_files(['tests/assets/example_file_1.ts.png','tests/assets/example_file_2.ts.png'])
    assert list(test_data.keys())==['tests/assets/example_file_1.ts.png','tests/assets/example_file_2.ts.png']
    