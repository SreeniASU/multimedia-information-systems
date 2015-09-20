import cv2
import os
from colormapcreation import createColorMap
from colormap2image import *

blackImage = cv2.imread(os.path.join(os.path.dirname(__file__), 'data/black.png'))
redImage = cv2.imread(os.path.join(os.path.dirname(__file__), 'data/red.png'))

def test_creates_black_image():
    # Test that creating an all black color map produces an all black
    # image regardless of the color space
    blackColorMap = createColorMap((0, 0, 0), (0, 0, 0), (0, 0, 0), 2)
    assert (colormap2image(blackColorMap, 'RGB') == blackImage).all()
    assert (colormap2image(blackColorMap, 'XYZ') == blackImage).all()
    assert (colormap2image(blackColorMap, 'Lab') == blackImage).all()
    assert (colormap2image(blackColorMap, 'Luv') == blackImage).all()
    assert (colormap2image(blackColorMap, 'YCrCb') == blackImage).all()
    assert (colormap2image(blackColorMap, 'HLS') == blackImage).all()
    assert (colormap2image(blackColorMap, 'HSV') == blackImage).all()

def test_creates_black_image_8_bits():
    # Test that creating an all black color map produces an all black
    # image regardless of the color space or bit
    blackColorMap = createColorMap((0, 0, 0), (0, 0, 0), (0, 0, 0), 8)
    assert (colormap2image(blackColorMap, 'RGB') == blackImage).all()
    assert (colormap2image(blackColorMap, 'XYZ') == blackImage).all()
    assert (colormap2image(blackColorMap, 'Lab') == blackImage).all()
    assert (colormap2image(blackColorMap, 'Luv') == blackImage).all()
    assert (colormap2image(blackColorMap, 'YCrCb') == blackImage).all()
    assert (colormap2image(blackColorMap, 'HLS') == blackImage).all()
    assert (colormap2image(blackColorMap, 'HSV') == blackImage).all()

def test_creates_solid_red():
    # Test that creating an all red color map in any color space
    # produces an a solid red image
    redRGBColorMap = createColorMap((255, 0, 0), (255, 0, 0), (255, 0, 0), 2)
    assert (colormap2image(redRGBColorMap, 'RGB') == redImage).all()
    redXYZColorMap = createColorMap((41.2400, 21.2600, 1.9300), (41.2400, 21.2600, 1.9300), (41.2400, 21.2600, 1.9300), 2)
    assert (colormap2image(redXYZColorMap, 'XYZ') == redImage).all()
    redLabColorMap = createColorMap((53.2329, 80.1093, 67.2201), (53.2329, 80.1093, 67.2201), (53.2329, 80.1093, 67.2201), 2)
    assert (colormap2image(redLabColorMap, 'Lab') == redImage).all()
    redHLSColorMap = createColorMap((0.00, 0.50, 1.00), (0.00, 0.50, 1.00), (0.00, 0.50, 1.00), 2)
    assert (colormap2image(blackColorMap, 'HLS') == blackImage).all()
    redHSVColorMap = createColorMap((0, 100, 100), (0, 100, 100), (0, 100, 100), 2)
    assert (colormap2image(blackColorMap, 'HSV') == blackImage).all()
