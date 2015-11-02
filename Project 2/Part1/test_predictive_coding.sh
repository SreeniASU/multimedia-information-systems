#!/usr/bin/env bash

python predictive_coding.py data/2.mp4 70 70 1
python predictive_coding.py data/2.mp4 70 70 2
python predictive_coding.py data/2.mp4 70 70 3
python predictive_coding.py data/2.mp4 70 70 4
mv *.tpc data
