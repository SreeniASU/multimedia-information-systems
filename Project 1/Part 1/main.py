# Team 6
# CSE 408 Project 1 - Part 2
#======================================
#Description:
#Implement a program that will allow the user to select
#- A color space
#- Three colors c0, c1, c2
#- Number of bits of storage
#given these
#- creates a colormap which maps each value in range -1 to +1 along the continuous path from c0 to c2 through c1 in 3D space.
#======================================
import re

import numpy as np
import cv2

import inquirer

def validColor(_, x):
    return re.match('^\d+, \d+, \d+$', x)

questions = [
    inquirer.List('colorSpace',
        message='What colorspace would you like to use?',
        choices=['RGB', 'XYZ', 'Lab', 'YUV', 'YCbCr', 'YIQ', 'HSL']
    ),
    inquirer.Text('c0',
        message='First color (must be in format 0, 133, 255)',
        validate=validColor
    ),
    inquirer.Text('c1',
        message='Second color',
        validate=validColor
    ),
    inquirer.Text('c2',
        message='Third color',
        validate=validColor
    ),
    inquirer.Text('b',
        message='Number of bits',
        validate=lambda _, x: re.match('\d+', x)
    )
]

print('======= Create a Custom Color Map =======')
answers = inquirer.prompt(questions)
