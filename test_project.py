from project import nacaParser, xValues, mkdir,meanCamberLine
from argparse import ArgumentTypeError
import pytest
import os

def test_nacaParser():
    assert nacaParser('154') == '0154'
    assert nacaParser('9999') == '9999'
    assert nacaParser('001') == '0001'
    with pytest.raises(ArgumentTypeError):
        nacaParser('asdjkl')
    with pytest.raises(ArgumentTypeError):
        nacaParser('10000')

def test_xValues():
    assert xValues(samples=2) == (0.0,0.5,1.0)
    assert xValues(samples=10) == (0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0)

def test_mkdir():
    path = 'testPATH123545609'
    # Make a dir in a defined path
    assert mkdir(path) == True
    # Try to make the same path
    assert mkdir(path) == False
    # Delete the path
    os.rmdir(path)


    
