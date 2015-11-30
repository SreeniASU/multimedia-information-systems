Each task of the project is in an individual python script that implements the specific functionality.

Task 1 a can be run from the command line with 

```
$ python block_quantize.py n ../path/to/file.mp4
```

Where n is the number of bins for the histograms, and the ../path/to/file.mp4 is the path to the desired video file.

Task 1 b can be run from the command line with 

```
$ python block_dct.py n ../path/to/file.mp4
```

Where n is the number of significant frequencies, and the ../path/to/file.mp4 is the path to the desired video file.

Task 1 c can be run from the command line with 

```
$ python block_dwt.py n ../path/to/file.mp4
```

Where n is the number of significant wavelets, and the ../path/to/file.mp4 is the path to the desired video file.

Task 1 d can be run from the command line with 

```
$ python diff_quantize.py n ../path/to/file.mp4
```

Where n is the number of bins for the histograms, and the ../path/to/file.mp4 is the path to the desired video file.

Task 2 can be run from the command line with 

```
$ python frame_dwt.py n ../path/to/file.mp4
```

Where n is the number of significant wavelets, and the ../path/to/file.mp4 is the path to the desired video file.

Task 3 can be run from the command line with 

```
$ python match_frame.py f n m ../path/to/file.mp4
```

Where f is the frame number to compare, where 1 is the first frame. n is the value used in the Task 1 features, m is the number of significant wavelets for Task 2 features, and the ../path/to/file.mp4 is the path to the desired video file.

