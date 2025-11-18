# RealSenseDepth

## Accompanying Guides and Documentation

**Make sure to read these before proceeding further!**

1. [Camera Descriptions](./docs/realsense/about_cameras.md)
2. [RealSense Viewer - Recording Streams (Optional)](./docs/realsense/realsense-viewer.md)
3. [Python Environments](./docs/processing/python_environments.md)


## Core Scripts

### Reading `.bag` Metadata

Run this script to understand what streams were active in a `.bag` file and their parameters.

<details>
<summary><strong>Related Scripts:</strong></summary>

- **`src/bag_metadata.py`**
</details>

<details>
<summary><strong>How to Use:</strong></summary>

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

### Recording `.bag` via Python

<details>
<summary><strong>Related Scripts:</strong></summary>

- **`src/record.py`**
</details>

<details>
<summary><strong>How to Use:</strong></summary>

This operation assumes that you are recording with only ONE device.

1. You must have a `.json` file that contains the metadata for the streams you want to record. For example, if you wanted to stream both depth and RGB (as BGR8), then you might have some file like this `example_meta.json`:

    ```json
    [
        {
            "type": "stream.color",
            "format": "format.bgr8",
            "width": 1280,
            "height": 720,
            "fps": 30
        },
        {
            "type": "stream.depth",
            "format": "format.z16",
            "width": 1280,
            "height": 720,
            "fps": 30
        }
    ]
    ```

2. Call the following script, which expects your bag file and an output filename

    ```bash
    python src/record.py <PATH/TO/.json> <PATH/TO/.bag>
    ```

    So for our `example_meta.json`, we might want to do this, which outputs the recording into `python_recording.bag`:

    ```bash
    python src/record.py ./example_meta.json ./python_recording.bag
    ```

</details>

<details>
<summary><strong>Expected Output:</strong></summary>

If successfully configured, you should see a `.bag` file outputted. You can preview this bag with the next set of instructions below.

</details>

---

### Previewing `.bag` File

<details>
<summary><strong>Related Scripts:</strong></summary>

- **`src/bag_metadata.py`**
- **`src/preview_bag.py`**
</details>

<details>
<summary><strong>How to Use:</strong></summary>

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
<summary><strong>How to Use:</strong></summary>

You must first run `bag_metadata.py` to output the stream metadata as a JSON file

```bash
python src/bag_metadata.py <PATH/TO/.bag> -o
```

Then, you can run `generate_videos.py` to preview the bag data itself

```bash
# Template Command
python src/generate_videos_bag.py <PATH/TO/.bag> <PATH/TO/.json> -s <DEPTH> <COLOR> -od <WIDTH> <HEIGHT>

# Example Command:
python src/generate_videos.py samples_ignore/capstone/20251116_155458.bag samples_ignore/capstone/20251116_155458.json -od 640 480
```

- `<PATH/TO/.bag>`: A local path to the `.bag` data you want to read.
- `<PATH/TO/.json>`: A local path to the `json` data that contains meta info about your `.bag` file
- `-s`: Which data streams should we output? Expects two separate outputs (e.g. `... -s depth width ...`). You can isolate the streams to just `depth` or `color` if you want.
- `-od`: The output dimensions of each video generated. Expects two separate integer values: `width` (in pixels), and `height` (in pixels). These are applied to both depth and color videos, if both are requested.
</details>

<details>
<summary><strong>Expected Output:</strong></summary>

- While the script is running, you will see temporary directories created. These temp directories store frames independently as images. There are complicated reasons for this. These temp directories can be memory intensive!
- When each video is generated, the temp directories will be deleted automatically.
- The videos generated will be saved in the same directory and filename as the original `.bag` file.
</details>