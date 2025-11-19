# Python Setup: Mac OSX

You are expected to have at least **Python Version 3.8** installed and accessible via your command line.

## Step 1. Installing the Correct Python Version

There are different strategies available to you. The easiest way from my experience is to use <a href="https://brew.sh/" target="_blank">`Homebrew`</a> and <a href="https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv" target="_blank">`pyenv`</a>.

<details>
<summary><strong>Installing `pyenv`:</strong></summary>

```bash
brew install pyenv
```
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


## Step 2: Setting Up a Virtual Environment

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
pip install -r requirements_mac.txt
```
</details>

<details>
<summary><strong>Deactivating the Virtual Env:</strong></summary>

```bash
deactivate
```
</details>