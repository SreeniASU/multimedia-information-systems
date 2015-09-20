import os
from colormapcreation import createColorMap

def test_making_black():
    # Test that passing just (0, 0, 0) three times at 2 bits
    # creates a colormap of (0,0,0), (0,0,0), (0,0,0), (0,0,0)
    colorMap = createColorMap((0, 0, 0), (0, 0, 0), (0, 0, 0), 2)
    assert colorMap == [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

def test_making_gradient():
    # Tests that you can create a white to red to black gradient
    # uses fixture WRB.txt for comparison
    colorMap = createColorMap((255, 255, 255), (255, 0, 0), (0, 0, 0), 8)
    file = open(os.path.realpath(os.path.join(os.path.dirname(__file__), 'data/WRB.txt')))
    assert colorMap == eval(file.read())
