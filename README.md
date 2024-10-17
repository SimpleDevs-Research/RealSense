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

Example command, which assumes you have a `.bag` file with the filename `depthcolor_15_rgb8-15.bag`. It's accessible here: [https://www.dropbox.com/scl/fo/ogvg2nla6r1waw49ieu8o/ANL7mDpgVC5rdLKAy1VUnqw?rlkey=eudzjgqvfvclzo01r7uu3o0b5&st=u115camp&dl=0](https://www.dropbox.com/scl/fo/ogvg2nla6r1waw49ieu8o/ANL7mDpgVC5rdLKAy1VUnqw?rlkey=eudzjgqvfvclzo01r7uu3o0b5&st=u115camp&dl=0)

```bash
python read_depth_and_color.py depthcolor_15_rgb8-15.bag 15 15 -cf rgb8
```

_Reading depth data only from Lidar, saving output file to video with increased resolution:_
```bash
python src/read_depth_and_color.py samples_ignore/L515/20241016_175610.bag -d -dr 320 240 -dfps 30 -df z16 -o -or 640 480 -ofps 30
```