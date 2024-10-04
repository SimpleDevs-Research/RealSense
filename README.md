# RealSenseDepth

## Installation

You must activate a virtual environment with the latest python version of 3.7. If you do not know how to do this, follow these instructions:

1. Make sure python 3.7 is installed on your machine. The easiest way to commonly do this is to use `py -0`, which lists all python installs on your local device. You can download the latest installer (3.7.9) on python's downloads page: [https://www.python.org/downloads/release/python-379/](https://www.python.org/downloads/release/python-379/)
2. Create a virtual environment with the following command, which creates a new virtual environment inside a folder named `realsense`. Unsure if it auto-creates the folder for you or not. If an error occurs, simply make an empty directory with the same name, then execute.
```
py -3.7 -m venv realsense
```
3. `cd` into `realsense/`, then activate the virtual environment. If you developed this on a Mac, the command will be different - make sure to look it up.
```
.\Scripts\activate.ps1
.\Scripts\activate.bat
```
4. Make sure the following packages are installed in this virtual environment:
    1. `numpy`
    2. `opencv-python`
    3. `pyrealsense2`

## Running the application

Example command, which assumes you have a `.bag` file with the filename `depthcolor_15_rgb8-15.bag`.
```
python read_depth_and_color.py depthcolor_15_rgb8-15.bag 15 15 -cf rgb8
```