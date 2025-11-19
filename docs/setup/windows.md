# Python Setup: Windows

You are expected to have at least **Python Version 3.8** installed and accessible via your command line.

## Step 1. Installing the Correct Python Version

If you don't have Python 3.8 installed, the easiest and hassle-free way to do this is to install Python 3.8 using an official installer. The installer for Python 3.8.20 is available <a href="https://www.python.org/downloads/release/python-3820/" target="_blank">on the official Python website</a>. Alternatively, you can search for all Python installers <a href="https://www.python.org/downloads/" target="_blank">on their "Downloads" page</a>.


<details>
<summary><strong>Check Installed Versions</strong></summary>

```bash
py -0
```
</details>

## Step 2: Setting Up a Virtual Environment

We want to set up a Python 3.8 virtual environment, such that we can isolate all package imports and python ops to a setting that works off of Python 3.8.

> Make sure to change your working directory to the folder where you will be working off of. If you cloned this repository, then you'll want to change the working directory to this repository's folder on your local drive.

We're going with the assumption you used an installer package to install the recommended Python version.

<details>
<summary><strong>Create the Virtual Env:</strong></summary>

```bash
py -3.8 -m venv [NAME OF ENVIRONMENT]
```
</details>

<details>
<summary><strong>Activate the Virtual Env:</strong></summary>

```bash
[NAME OF ENVIRONMENT]/Scripts/activate.ps1
```
</details>


<details>
<summary><strong>Installing Dependencies:</strong></summary>

```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>Deactivating the Virtual Env:</strong></summary>

```bash
deactivate
```
</details>