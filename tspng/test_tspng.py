#!/usr/bin/env python3

from extraction import extraction

def test_hello_world():
    print('Hello World!')

def test_extraction():
    test_data = extraction('tests/assets/example_file.ts.png')
    assert list(test_data.keys())==['info','licenses','images','annotations','models','categories']
