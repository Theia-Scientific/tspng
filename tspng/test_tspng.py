#!/usr/bin/env python3

from . import add

def test_hello_world():
    print('Hello World!')

def test_add():
    assert add(1,1)==2
