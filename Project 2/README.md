# Project 2 - Team 6

**Gabriel, Jake, Sreeni, Derek, James**

This project was implemented in Python, using the OpenCV library for video reading/writing as well as the numpy library for large array operations. Each part of the assignment is broken into its respective Parts, corresponding with

- Part1 - Temporal Predictive Coding
- Part2 - Spatial Predictive Coding
- Part3 - Quantization
- Part4 - Lossless compression
- Part5 - Decoding to video

Each part can be run independently by executing the python script in each of the folders. To run all of the parts together on the same video, run the executable

```
python encode.py
```

This will prompt you for all of the information necessary to code, quantize, and compress a video file to a `.tpv` or `.spv` file and all of the files in between.

In order to turn any file into a video in `.avi` format, run the single python script

```
pthon toVideo.py
```

and pass the full path of the compressed file as the first argument. The file can be any of the intermediate file types or the final type, very useful for debugging encoding and decoding.

## Troubleshooting

If you are experiencing issues with getting the code to run, first check that python and opencv are installed correctly. Run the following in your terminal:

```
$ python
>>> import numpy
>>> import cv2
```

If this throws errors, you may need to reinstall python and opencv.

If you experience errors when working through the prompts of `encode.py` or `toVideo.py`, make sure you are providing full absolute paths for the directories.

If you cannot find the video files or intermediate files, look in the folder of `encode.py` and the folder of your original `.mp4` file.

In the event that the code doesn't work, please feel free to send me an email at jrpruit1@asu.edu.
