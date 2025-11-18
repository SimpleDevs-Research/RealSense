# RealSenseDepth

## Accompanying Guides and Documentation

**Make sure to read these before proceeding further!**

1. [Camera Descriptions](./docs/realsense/about_cameras.md)
2. [RealSense Viewer - Recording Streams](./docs/realsense/realsense-viewer.md)
3. [Python Environments](./docs/processing/python_environments.md)


## Core Scripts

### Reading `.bag` Metadata

Run this script to understand what streams were active in a `.bag` file and their parameters.

<details>
<summary><strong>Related Scripts:</strong></summary>

- **`src/bag_metadata.py`**
</details>

<details>
<summary><strong>Commands:</strong></summary>

```bash
python src/bag_metadata.py <PATH/TO/.bag> -o
```

- `<PATH/TO/.bag>`: A local path to the `.bag` data you want to read.
- `-o`: Output the metadata as a JSON file, with the same filename and same location as the provided `.bag` file.
</details>

<details>
<summary><strong>Example Output:</strong></summary>

```
Streams found:
- TYPE: stream.depth             RES: 1280x720 @ 30 FPS          FORMAT: format.z16
- TYPE: stream.color             RES: 1280x720 @ 30 FPS          FORMAT: format.rgb8
Metadata outputted to `samples_ignore/capstone\20251116_155458.json`
```
</details>

---

### Previewing `.bag` File

<details>
<summary><strong>Related Scripts:</strong></summary>

- **`src/bag_metadata.py`**
- **`src/preview_bag.py`**
</details>

<details>
<summary><strong>Commands:</strong></summary>

You must first run `bag_metadata.py` to output the stream metadata as a JSON file
```bash
python src/bag_metadata.py <PATH/TO/.bag> -o
```

Then, you can run `preview_bag.py` to preview the bag data itself
```bash
python src/preview_bag.py <PATH/TO/.bag> <PATH/TO/.json> -rp
```

- `<PATH/TO/.bag>`: A local path to the `.bag` data you want to read.
- `<PATH/TO/.json>`: A local path to the `json` data that contains meta info about your `.bag` file
- `-rp`: When previewing the bag data, do you want the streams to repeat in a loop?
</details>

<details>
<summary><strong>Expected Output:</strong></summary>

- You will see an OpenCV window pop up showing the frames. The frames are aligned in script. 
- However, this doesn't mean that you'll see ALL frames, as the stream may skip frames sometimes. 
- You can close the window by pressing the "Escape" key on your keyboard while the preview window is selected.
- This script does NOT produce a video for you. For that, look at the next script
</details>

---

### Generating Videos

<details>
<summary><strong>Related Scripts:</strong></summary>

- **`src/bag_metadata.py`**
- **`src/generate_videos.py`**
</details>

<details>
<summary><strong>Commands:</strong></summary>

You must first run `bag_metadata.py` to output the stream metadata as a JSON file

```bash
python src/bag_metadata.py <PATH/TO/.bag> -o
```

Then, you can run `generate_videos.py` to preview the bag data itself

```bash
# Template Command
python src/generate_videos_bag.py <PATH/TO/.bag> <PATH/TO/.json> -s <DEPTH> <COLOR> -od <WIDTH> <HEIGHT> <FPS>

# Example Command:
python src/generate_videos.py samples_ignore/capstone/20251116_155458.bag samples_ignore/capstone/20251116_155458.json -od 640 480 15
```

- `<PATH/TO/.bag>`: A local path to the `.bag` data you want to read.
- `<PATH/TO/.json>`: A local path to the `json` data that contains meta info about your `.bag` file
- `-s`: Which data streams should we output? Expects two separate outputs (e.g. `... -s depth width ...`). You can isolate the streams to just `depth` or `color` if you want.
- `-od`: The output dimensions of each video generated. Expects three separate integer values. These are applied to both depth and color videos, if both are requested.
</details>

<details>
<summary><strong>Expected Output:</strong></summary>

- While the script is running, you will see temporary directories created. These temp directories store frames independently as images. There are complicated reasons for this. These temp directories can be memory intensive!
- When each video is generated, the temp directories will be deleted automatically.
- The videos generated will be saved in the same directory and filename as the original `.bag` file.
</details>