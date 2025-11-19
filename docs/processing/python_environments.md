# Preparing Python Environments

## Step 1. Installing the Correct Python Version

You are expected to have **Python Version 3.7** installed and accessible via your command line. How you install this will differ between device type.

<details>
<summary><strong>Windows PC</strong></summary>

To double-check the python versions already installed on your device, you can use the following command:

```bash
py -0
```

If you don't have Python3.7 installed, the easiest and hassle-free way to do this is to install Python 3.7 using an official installer. The installer for Python3.7 is available <a href="https://www.python.org/downloads/release/python-379/" target="_blank">on the official Python website</a>.
</details>

<details>
<summary><strong>Macintosh OS X</strong></summary>

There are different strategies available to you. The easiest way from my experience is to use <a href="https://brew.sh/" target="_blank">**Homebrew**</a> and <a href="https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv" target="_blank">**pyenv**</a>.

At that point, once you have **pyenv** installed, you can then install Python3.7 using the following command:

```bash
pyenv install 3.7
```

</details>


<details>
<summary><strong>Linux</strong></summary>

The easiest way from my experience is to use <a href="https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv" target="_blank">**pyenv**</a>. However, the process to install this is a bit different on Linux and Ubuntu-based systems. This part of the documentation is inspired by <a href="https://www.digikey.de/de/maker/tutorials/2024/how-to-manage-multiple-python-installations-on-raspberry-pi" target="_blank">DigiKey</a>.

Firstly, you must install **pyenv** via `apt`:

```bash
curl https://pyenv.run | bash
```

This process isn't long, but you must follow an additional step to make sure you can call **pyenv** via your Terminal. 

1. Locate your `~/.bashrc` file, which is usually located at `/home/<username>/.bashrc`.
2. Add the following lines to the end of the document, and save:

    ```bash
    export PATH="$HOME/.pyenv/bin:$PATH"
    export PYENV_ROOT="$HOME/.pyenv"
    eval "$(pyenv init --path)"
    eval "$(pyenv virtualenv-init -)"
    ```
3. Close your bash terminals and reopen. This causes the bash environment to recognize commands such as `pyenv`.

At this point, you can then install Python3.7 using the following command:

```bash
pyenv install 3.7
```

You will face additional barriers, such as missing packages. If you encounter such messages, then just import them via `sudo apt` and re-install the python version again.

</details>

## Step 2: Setting Up a Virtual Environment

We want to set up a Python3.7 virtual environment, such that we can isolate all package imports and python ops to a setting that works off of Python3.7. The steps to do this are different between Windows and OS X.

> Make sure to change your working directory to the folder where you will be working off of. If you cloned this repository, then you'll want to change the working directory to this repository's folder on your local drive.

<details>
<summary><strong>Windows PC</strong></summary>

This assumes that you've installed Python3.7 using an official Python installer. The commands to create and run a Python3.7 environment are the following:

```bash
# Create your virtual environment; creates a folder with the same name
py -3.7 -m venv <NAME OF ENVIRONMENT>

# Run the environment itself
<NAME OF ENVIRONMENT>/Scripts/activate.ps1
```

For example, let's say we want to create and run a virtual environment called `realsense_env`. The commands will look like this:

```bash
py -3.7 -m venv realsense_env
realsense_env/Scripts/activate.ps1
```

</details>

<details>
<summary><strong>Mac OS X</strong></summary>

We're going with the assumption you used **Homebrew** and **pyenv** to install Python3.7. From that, we need to install an additional package via Homebrew: **pyenv-virtualenv**.

```bash
brew install pyenv-virtualenv
```

After that, you can create and run a new virtual environment using Python3.7 using the following commands:

```bash
pyenv virtualenv 3.7 <NAME OF ENVIRONMENT>
pyenv activate <NAME OF ENVIRONMENT>
```

For example, if we wanted to create a virtual environment called `realsense_env`, then we'd run the following commands:

```bash
pyenv virtualenv 3.7 realsense_env
pyenv activate realsense_env
```

</details>

<details>
<summary><strong>Linux</strong></summary>

We're going with the assumption you used **pyenv** to install Python3.7. From that, we need to install an additional package: **pyenv-virtualenv**.

```bash
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
```

After that, you can create and run a new virtual environment using Python3.7 using the following commands:

```bash
pyenv virtualenv 3.7 <NAME OF ENVIRONMENT>
pyenv activate <NAME OF ENVIRONMENT>
```

If you run into an error where you get a message like this:

```
`pyenv activate' requires Pyenv and Pyenv-Virtualenv to be loaded into your shell.
Check your shell configuration and Pyenv and Pyenv-Virtualenv installation instructions.
```

An alternative way to activate your environment is to use the following command:

```bash
# Don't forget that `.` at the beginning!
. ${PYENV_ROOT}/versions/<NAME OF ENVIRONMENT>/bin/activate
```

</details>

<details>
<summary><strong>Deactivating your environment</strong></summary>

To deactivate your Python environment, just use this basic command:

```bash
deactivate
```

</details>

## Step 3: Installing Dependencies

While your Python environment is running, you need to install the necessary Python packages. The required packages are mentioned in two separate files: `requirements_windows.txt` for Windows, and `requirements_mac.txt` for Mac OS X. We need two separate versions because one of the packages, <a href="https://pypi.org/project/pyrealsense2/" target="_blank">`pyrealsense2`</a>, only works on Windows PC. There is a Mac OS X equivalent: <a href="https://pypi.org/project/pyrealsense2-mac/" target="_blank">`pyrealsense2-mac`</a>.

Depending on whichever OS you are using, here's a one-liner command you can use:

```bash
pip install -r requirements_windows.txt # For Windows PCs
pip install -r requirements_mac.txt     # For Mac OS X
```