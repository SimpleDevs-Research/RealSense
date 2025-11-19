# Python Setup: Linux / Ubuntu

This step is a bit different from the Windows or OSX installation. This is because the `librealsense` and `pyrealsense2` packages are not really designed to work on Linux- or Ubuntu-based systems. This guide will be much more detailed in its instructions.

> **NOTE**: This guide will be _immensely_ time-consuming! Be prepared to wait a long time for some of these steps.

## Step 1. Installing Prerequisites

<details>
<summary><strong>Update your Libraries:</strong></summary>

```bash
sudo apt update
sudo apt upgrade -y
```
</details>

<details>
<summary><strong>Install Prereqs:</strong></summary>

```bash
sudo apt install -y \
    git cmake build-essential pkg-config \
    libusb-1.0-0-dev libssl-dev \
    libopencv-dev   \
    libglfw3-dev libglew-dev xorg-dev \
    libgtk-3-dev libgl1-mesa-dev udev
```
</details>

## Step 2. Installing the Correct Python Version

The easiest way from my experience is to use <a href="https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv" target="_blank">**pyenv**</a>. This part of the documentation is inspired by <a href="https://www.digikey.de/de/maker/tutorials/2024/how-to-manage-multiple-python-installations-on-raspberry-pi" target="_blank">DigiKey</a>.

<details>
<summary><strong>Install `pyenv`</strong></summary>

1. Install `pyenv` via `curl`:
    ```bash
    curl https://pyenv.run | bash
    ```

2. Locate your `~/.bashrc` file, which is usually located at `/home/[USERNAME]/.bashrc`.
3. Add the following lines to the end of the document, and save:

    ```bash
    export PATH="$HOME/.pyenv/bin:$PATH"
    export PYENV_ROOT="$HOME/.pyenv"
    eval "$(pyenv init --path)"
    eval "$(pyenv virtualenv-init -)"
    ```
4. Close all bash terminals and reopen. This causes the bash environment to recognize commands such as `pyenv`.
</details>

<details>
<summary><strong>Installing Python 3.8:</strong></summary>

```bash
pyenv install 3.8   # Install
pyenv versions      # Confirm
```
</details>

<details>
<summary><strong>Switching to Python 3.8 in the current Shell:</strong></summary>

```bash
pyenv global 3.8.16
pyenv shell 3.8.16  
python3 --version   # Confirm
python --version    # Confirm
```
</details>


## Step 3: Setting Up a Virtual Environment

We want to set up a Python 3.8 virtual environment, such that we can isolate all package imports and python ops to a setting that works off of Python 3.8.

> Make sure to change your working directory to the folder where you will be working off of. If you cloned this repository, then you'll want to change the working directory to this repository's folder on your local drive.

We're going with the assumption you used **Homebrew** and **pyenv** to install Python 3.8.

<details>
<summary><strong>Create the Virtual Env:</strong></summary>

```bash
python3 -m venv [NAME OF ENVIRONMENT]
```
</details>

<details>
<summary><strong>Activate the Virtual Env:</strong></summary>

```bash
source [NAME OF ENVIRONMENT]/bin/activate
# or
. [NAME OF ENVIRONMENT]/bin/activate
```
</details>

<details>
<summary><strong>Installing Dependencies:</strong></summary>

```bash
pip install -r requirements_linux.txt
```

> You might notice that we aren't installing `pyrealsense2` like with other installation guides. This will be covered in the next section.
</details>

<details>
<summary><strong>Deactivating the Virtual Env:</strong></summary>

```bash
deactivate
```
</details>

## Step 4: Installing Librealsense v2.50.0

In the Windows and OSX installation guides, we merely installed `pyrealsense2` or `pyrealsense2-macosx` via `pip`. However, that's not going to work on Linux. This is due to USB permissions. I've had a lot of difficulty trying to get our RealSense cameras to get detected by the `pip`-installed versions of `pyrealsense2` on Linux. 

The alternative therefore is to literally _build_ `pyrealsense2` from the <a href="https://github.com/IntelRealSense/librealsense/releases/tag/v2.50.0" target="_blank">v2.50.0 release of the `librealsense` SDK</a>. So make sure to follow these instructions **VERY CAREFULLY**.

<details>
<summary><strong>Clone / Download `librealsense` v2.50.0</strong></summary>

1. This is just as simple as downloading the source code `.zip` from <a href="https://github.com/IntelRealSense/librealsense/releases/tag/v2.50.0" target="_blank">the release page</a>.
2. Place it in a location that's easy to access - e.g. the Desktop.
</details>

<details>
<summary><strong>Preparing `cmake`:</strong></summary>

1. Change the working directory to the newly-downloaded `librealsense-2.50.0` folder:

    ```bash
    cd [PATH/TO/]librealsense-2.50.0
    ```
2. Prep building using `cmake`

    ```bash
    mkdir build && cd build
    
    cmake .. \
    -DBUILD_PYTHON_BINDINGS=ON \
    -DPYTHON_EXECUTABLE=$(pyenv which python) \
    -DBUILD_EXAMPLES=ON \
    -DFORCE_RSUSB_BACKEND=ON \
    -DBUILD_SHARED_LIBS=ON
    ```

    **Explanation of Flags:**
    |Flag|Description|
    |:--|:--|
    |`BUILD_PYTHON_BINDINGS=ON`|Required for `pyrealsense2`|
    |`PYTHON_EXECUTABLE=$(pyenv which python)`|Links bindings to your pyenv Python|
    |`FORCE_RSUSB_BACKEND=ON`|Required on Raspberry Pi (no kernel patches)|
    |`BUILD_SHARED_LIBS=ON`|Needed for Python dynamic loading|
    |`BUILD_EXAMPLES=ON`|Allows building realsense-viewer|

</details>

<details>
<summary><strong>Compile and Build w/ `cmake`:</strong></summary>

```bash
make -j2            # Or just `make`, or `make -j4`.
sudo make install   # Install into the system
```
</details>

## Step 5: Linking `librealsense` and the Virtual Environment

With the `pyrealsense2` version now built using `librealsense`, let's now make sure that the Virtual Environment we created in Step 3 works with that built version.

<details>
<summary><strong>Locating `.so`</strong></summary>

When we built `pyrealsense`, it generated a `.so` file. We need to locate that `.so` file. We can do so easily with this command:

```bash
find . -name "pyrealsense2*.so"
```

You should see something similar to the following. You should be looking within the `wrappers/` directory inside the `build/` folder you are currently `cd`-ed in:

```
wrappers/python/pyrealsense2.cpython-38-arm-linux-gnueabihf.so
```
</details>

<details>
<summary><strong>Copying `.so` Into the Virtual Env:</strong></summary>

We're assuming you are still in the `build` directory and the virtual environment folder we generated in Step 3 is located inside of `Desktop/RealSense` git repo folder:

```bash
cp ./wrappers/python/pyrealsense2*.so \
   ~/Desktop/RealSense/[NAME OF ENVIRONMENT]/lib/python3.8/site-packages/
```

You can verify that this was succesful with the following command:

```bash
ls ~/Desktop/RealSense/[NAME OF ENVIRONMENT]/lib/python3.8/site-packages/pyrealsense2*.so
```
</details>

<details>
<summary><strong>Testing:</strong></summary>

Activate your virtual environment, and try running the following command:

```bash
python - << 'EOF'
import pyrealsense2 as rs
print("Loaded:", rs.__file__)
ctx = rs.context()
print("Devices:", ctx.query_devices())
EOF
```
</details>