import argparse
import numpy as np
import cv2
import os
import json
import platform
system = platform.system()
if system == "Darwin": # Mac OSX
    import pyrealsense2_mac as rs
else:
    import pyrealsense2 as rs

# Parse arguments
parser = argparse.ArgumentParser(
    description="Read a `.bag` file and its metadata file to \
                preview the stream contents captured in the recording.")
parser.add_argument("input_bag", 
                    type=str, 
                    help="Path to the bag file")
parser.add_argument("input_metadata",
                    type=str,
                    help="Path to the metadata file associated with the bag file")
parser.add_argument("-rp", "--repeat_playback",
                    action="store_true",
                    help="Should the preview repeat the playback in a loop?")
args = parser.parse_args()

# Check if provided files actually exist
assert os.path.exists(args.input_bag), "Input .bag file not detected."
assert os.path.exists(args.input_metadata), "Input .json metadata file not detected"

# Initialize a pipeline to read the bag file
pipeline = rs.pipeline()
config = rs.config()
config.enable_device_from_file(args.input_bag, repeat_playback=args.repeat_playback)

# Read the provided metadata, enable the streams in our config
_STREAM_TYPES = {
    'stream.depth': rs.stream.depth,
    'stream.color': rs.stream.color
}
_STREAM_FORMATS = {
    'format.z16': rs.format.z16,
    'format.rgb8': rs.format.rgb8,
    'format.bgr8': rs.format.bgr8,
    'format.yuyv': rs.format.yuyv
}
with open(args.input_metadata, "r") as f:
    streams_raw = json.load(f)
    streams = []
    color_exists = False
    for stream in streams_raw:
        rs_type = _STREAM_TYPES[stream['type']]
        rs_format = _STREAM_FORMATS[stream['format']]
        config.enable_stream(rs_type, stream['width'], stream['height'], rs_format, stream['fps'])
        streams.append({ **stream, "rs.type":rs_type, "rs.format":rs_format })
        if stream['type'] == 'stream.color': color_exists = True

# Initialize Frame Aligner, for aligning frames. We force the frames to align to the RGB component if it exists; otherwise, use the first stream in `streams`
align_to = rs.stream.color if color_exists else streams[0]['rs.type']
frame_aligner = rs.align(align_to)

# Initialize a colorizer to visualize the depth color
frame_colorizer = rs.colorizer()

# Read the streams, output what kind of stream types they each are
profile = pipeline.start(config)

# Create a preview window
cv2.namedWindow("Depth and Color Stream", cv2.WINDOW_AUTOSIZE)

# Start iterating through frames
while True:
    # Wait for frames. If frames don't exist anymore, exit early
    frame_present, frames = pipeline.try_wait_for_frames()
    if not frame_present:
        print("Frames no longer present!")
        break

    # Apply alignment
    aligned_frames = frame_aligner.process(frames)

    # Get aligned frames. We only extract ones dependent on available streams
    extracted_frames = []
    for stream in streams:
        _frame_type = stream['type']
        if _frame_type == 'stream.depth': 
            _frame = aligned_frames.get_depth_frame()
            color_frame = frame_colorizer.colorize(_frame)
            depth_image = np.asanyarray(color_frame.get_data())
            depth_dims = depth_image.shape
            extracted_frames.append({'type':_frame_type, 'frame':depth_image, 'dims':depth_dims})
        elif _frame_type == 'stream.color': 
            _frame = aligned_frames.get_color_frame()
            color_image = np.asanyarray(_frame.get_data())
            color_dims = color_image.shape
            extracted_frames.append({'type':_frame_type, 'frame':color_image, 'dims':color_dims})

    # If there are no extracted frames, then we skip
    if len(extracted_frames) == 0: continue

    # Assuming there are frames, we match the dimensions to those of the smallest
    smallest = min(extracted_frames, key=lambda o: o["dims"][0])['dims']
    resized_frames = [ cv2.resize(frame['frame'], dsize=(smallest[1], smallest[0]), interpolation=cv2.INTER_AREA) for frame in extracted_frames]
    rendered_image = np.hstack(resized_frames)

    # Render the image, make sure to add a quitter operation for early exits
    cv2.imshow("Depth and Color Stream", rendered_image)
    key = cv2.waitKey(1)
    # if pressed escape exit program
    if key == 27:
        cv2.destroyAllWindows()
        break

# Stop the pipeline
pipeline.stop()

