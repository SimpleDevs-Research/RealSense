# Python Setup: Linux / Ubuntu

This step is a bit different from the Windows or OSX installation. This is because the `librealsense` and `pyrealsense2` packages are not really designed to work on Linux- or Ubuntu-based systems. This guide will be much more detailed in its instructions.

> **NOTE**: This guide will be _immensely_ time-consuming! Be prepared to wait a long time for some of these steps.

## Step 1. Installing the Correct Python Version

The easiest way from my experience is to use <a href="https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv" target="_blank">**pyenv**</a>. This part of the documentation is inspired by <a href="https://www.digikey.de/de/maker/tutorials/2024/how-to-manage-multiple-python-installations-on-raspberry-pi" target="_blank">DigiKey</a>.

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
sudo apt install git cmake libssl-dev libusb-1.0-0-dev pkg-config udev -y
```
</details>

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
pyenv shell 3.8.16
python3 --version
```
</details>

## Step 2: Installing Librealsense v2.50.0

In the Windows and OSX installation guides, we merely installed `pyrealsense2` or `pyrealsense2-macosx` via `pip`. However, that's not going to work on Linux. This is due to USB permissions. I've had a lot of difficulty trying to get our RealSense cameras to get detected by the `pip`-installed versions of `pyrealsense2` on Linux. 

The alternative therefore is to literally _build_ `pyrealsense2` from the <a href="https://github.com/IntelRealSense/librealsense/releases/tag/v2.50.0" target="_blank">v2.50.0 release of the `librealsense` SDK</a>. So make sure to follow these instructions **VERY CAREFULLY**.

<details>
<summary><strong>Clone / Download the original source of `librealsense` v2.50.0</strong></summary>

1. This is just as simple as downloading the source code `.zip` from <a href="https://github.com/IntelRealSense/librealsense/releases/tag/v2.50.0" target="_blank">the release page</a>.
2. Place it in a location that's easy to access - e.g. the Desktop.
</details>

<details>
<summary><strong>Building `librealsense`</strong></summary>

1. Change the working directory to the newly-downloaded `librealsense-2.50.0` folder:

    ```bash
    cd [PATH/TO/]librealsense-2.50.0
    ```
2. Prep building using `cmake`

    ```bash
    mkdir build && cd build
    
    ```


</details>