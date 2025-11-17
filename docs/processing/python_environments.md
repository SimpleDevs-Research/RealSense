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
</details>

## Step 2: Setting Up a Virtual Environment

We want to set up a Python3.7 virtual environment, such that we can isolate all package imports and python ops to a setting that works off of Python3.7. The steps to do this are different between Windows and OS X.

> Make sure to change your working directory to the folder where you will be working off of. If you cloned this repository, then you'll want to change the working directory to this repository's folder on your local drive.

Assuming you installed Python3.7, you should have access to the `python3` command. To create a python environment, follow this general structure:

```bash
python3 -m venv <NAME OF ENVIRONMENT>
```

For example, let's say we want to create a virtual environment called `realsense_env`. The command to create this environment is:

```bash
python3 -m venv realsense_env
```

if successful, you should see a new folder in your current directory with the same name as your environment.

## Step 3: Activating (and Deactivating) the Python Environment

The commands to activate your new Python environment differ between Windows PC and OS X. These examples assume you created a `realsense_env` virtual environment, like in the example in the previous step.

<details>
<summary><strong>Windows PC</strong></summary>

```bash
realsense_env/Scripts/activate.ps1
```

</details>

<details>
<summary><strong>Macintosh OS X</strong></summary>

```bash
source realsense_env/bin/activate
```

</details>

<details>
<summary><strong>Deactivating your environment</strong></summary>

To deactivate your Python environment, just use this basic command:

```bash
deactivate
```

</details>

## Step 4: Installing Dependencies

While your Python environment is running, you need to install the necessary Python packages. The required packages are mentioned in `requirements.txt`, but for simplicity you can import them all using this simple command:

```bash
pip install -r requirements.txt
```