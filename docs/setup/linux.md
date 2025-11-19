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
