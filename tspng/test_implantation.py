#!/usr/bin/env python3

import os
import pathlib
import pytest

from io import BytesIO
from tspng.implantation import implant,implant_to_file
from tspng.extraction import extract

def test_implant():
    '''
    Tests the dictionary keys from an example TSPNG file path.
    '''
    #test file
    implant('tests/assets/coco_data.txt','tests/assets/empty.png')
    #test_data = extract('tests/assets/coco_data.txt+tests/assets/empty.png')
    test_data = extract('tests/assets/empty.png')
    assert list(test_data.keys())==['info','licenses','images','annotations','models','categories']

def test_implant_fails():
    with pytest.raises(TypeError):
        implant('Test for failure')

def test_implant_to_file():
    '''
    Tests the dictionary keys from an example TSPNG file path.
    '''
    implant_to_file('tests/assets/coco_data.txt','tests/assets/empty.png')
    #test_data = extract('tests/assets/coco_data.txt+tests/assets/empty.png')
    test_data = extract('tests/assets/empty.png')
    assert list(test_data.keys())==['info','licenses','images','annotations','models','categories']

def test_implant_to_file_fails():
    #test folder instead of file
    with pytest.raises(Exception):
        implant_to_file('Random/path.png')
    #test file does not exist
    with pytest.raises(Exception):
        implant_to_file('tests/assets')
