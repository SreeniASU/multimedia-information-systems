# multimedia-information-systems

Repository for code and reports for CSE 408/598 projects.

## Setup

To run the project executables, make sure [Python 2.7]() and [OpenCV](http://opencv.org/) are installed.

### On OS X

```bash
$ brew doctor
$ brew install python
$ brew install homebrew/science/opencv
```

### On Linux

```bash
$ sudo apt-get install python opencv
```

### On Windows

Follow the directions [in the OpenCV documentation](http://docs.opencv.org/doc/tutorials/introduction/windows_install/windows_install.html).

### Check that everything works

To make sure your installation has worked, open your terminal or powershell application and do the following commands:

```bash
$ python
>>> import cv
>>> import numpy
```

You should not see any warnings from the above commands. If you do see any warnings, contact Jake Pruitt (@jakepruitt) at (219) 921-4832, and I'll do my best to make sure it works for you.

## Testing

Tests use [pytest](http://pytest.org/latest/) for all tests. In order to run tests, first install pytest:

```bash
$ pip install pytest
```

Then, to run all of the tests, run the following command:

```bash
$ py.test
```
