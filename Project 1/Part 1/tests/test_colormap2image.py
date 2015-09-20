import cv2
import os
from colormapcreation import createColorMap
from colormap2image import *

blackImage = cv2.imread(os.path.realpath(os.path.join(os.path.dirname(__file__), 'data/black.jpg')))

def test_creates_black_image():
    # Test that creating an all black color map produces an all black
    # image regardless of the color space
    blackColorMap = createColorMap((0, 0, 0), (0, 0, 0), (0, 0, 0), 2)
    assert (colormap2image(blackColorMap, 'RGB') == blackImage).all()
