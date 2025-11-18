import argparse
import numpy as np
import cv2
import os
import json
from random import choice
from string import ascii_uppercase
import shutil
import gc
import platform
system = platform.system()
if system == "Darwin": # Mac OSX
    import pyrealsense2_mac as rs
else:
    import pyrealsense2 as rs

# Parse arguments
parser = argparse.ArgumentParser(
    description="Read a `.bag` file and its metadata file to \
                generate one or more videos of the stream contents captured in the recording.")
parser.add_argument("input_bag", 
                    type=str, 
                    help="Path to the bag file")
parser.add_argument("input_metadata",
                    type=str,
                    help="Path to the metadata file associated with the bag file")
parser.add_argument('-s', '--streams', 
                    nargs='+',
                    type=str,
                    choices=['depth', 'color'],
                    default=['depth', 'color'],
                    help="Explicitly define which streams to output as videos")
parser.add_argument('-od', '--output_dims',
                    nargs=3,
                    type=int,
                    default=[640, 480, 15],
                    help='The dimension (width, height, fps) of the expected output videos')
args = parser.parse_args()

# Check if provided files actually exist
assert os.path.exists(args.input_bag), "Input .bag file not detected."
assert os.path.exists(args.input_metadata), "Input .json metadata file not detected"

# Initialize a pipeline to read the bag file
pipeline = rs.pipeline()
config = rs.config()
config.enable_device_from_file(args.input_bag, repeat_playback=False)

# Generate some helper functions for helping us generate temporary output directories for each stream
def mkdirs(query_dir:str, delete_existing:bool=True):
    if delete_existing and os.path.exists(query_dir): 
        shutil.rmtree(query_dir)            # If the folder already exists, delete it
    os.makedirs(query_dir, exist_ok=True)   # Create a new empty directory
    return query_dir                        # Return the directory to indicate completion

def create_random_str(length:int = 12):
    return ''.join(choice(ascii_uppercase) for i in range(length))

# Read the provided metadata, enable the streams in our config
_STREAM_TYPES = {
    'stream.depth': rs.stream.depth,
    'stream.color': rs.stream.color
}
_STREAM_FORMATS = {
    'format.z16': rs.format.z16,
    'format.rgb8': rs.format.rgb8,
    'foramt.bgr8': rs.format.bgr8,
    'format.yuyv': rs.format.yuyv
}

streams = {}
with open(args.input_metadata, "r") as f:
    streams_raw = json.load(f)
    color_exists = False
    for stream in streams_raw:
        rs_type = _STREAM_TYPES[stream['type']]
        rs_format = _STREAM_FORMATS[stream['format']]

        # Check that if we want this stream to actually be used or not
        if stream['type'].split('.')[1] not in args.streams: 
            print(f"Skipping Stream {stream['type']}")
            continue

        config.enable_stream(rs_type, stream['width'], stream['height'], rs_format, stream['fps'])
        streams[stream['type']] = { **stream, "rs.type":rs_type, "rs.format":rs_format, 'temp_dir':mkdirs(create_random_str()+'_ignore'), 'frames_cache':[] }
        if stream['type'] == 'stream.color': color_exists = True
        print(f"Adding stream {stream['type']} as dictated via command arguments")

# Consider the case that no streams were considred
assert len(streams) > 0, "No streams are set for being outputted... Modify your command line arguments to fix this, specifically `-s` or `--streams`"

# Initialize Frame Aligner, for aligning frames. We force the frames to align to the RGB component if it exists; otherwise, use the first stream in `streams`
align_to = rs.stream.color if color_exists else next(iter(streams.values()))['rs.type']
frame_aligner = rs.align(align_to)

# Initialize a colorizer to visualize the depth color
frame_colorizer = rs.colorizer()

# Read the streams, output what kind of stream types they each are
profile = pipeline.start(config)
gc.disable()

# Start iterating through frames
print("Reading `.bag` data...")
while True:
    # Wait for frames. If frames don't exist anymore, exit early
    frame_present, frames = pipeline.try_wait_for_frames()
    if not frame_present:
        print("Frames no longer present!")
        break

    # Apply alignment
    aligned_frames = frame_aligner.process(frames)

    # Get aligned frames. We only extract ones dependent on available streams
    for stream_type in streams:
        # get the stream itself
        stream = streams[stream_type]
        
        # Handle different cases of stream types
        if stream_type == 'stream.depth': 
            # Get the image, and colorize since it's a depth image
            _frame = aligned_frames.get_depth_frame()
            color_frame = frame_colorizer.colorize(_frame)
            _image = np.asanyarray(color_frame.get_data())
            _frame_number = _frame.get_frame_number()
        elif stream_type == 'stream.color': 
            _frame = aligned_frames.get_color_frame()
            _image = np.asanyarray(_frame.get_data())
            _frame_number = _frame.get_frame_number()

        # Resize the iamge to fit the output dimensions
        resized_img = cv2.resize(_image, (args.output_dims[0], args.output_dims[1]), interpolation=cv2.INTER_AREA)

        # Save and Cache
        out_filename = os.path.join(stream['temp_dir'], f'{_frame_number}.png')
        streams[stream_type]['frames_cache'].append([_frame_number, out_filename])
        cv2.imwrite(out_filename, resized_img)
           
    # Make sure to add a quitter operation for early exits
    key = cv2.waitKey(1)
    # if pressed escape exit program
    if key == 27:
        break

# Stop the pipeline
pipeline.stop()
gc.enable()

# Generate an output basename for each stream
filename_root, file_extension = os.path.splitext(args.input_bag)
dirname = os.path.dirname(filename_root)
filename = os.path.basename(filename_root) 

# Now, with each frame cache saved, let's sort each and then print them as actual videos
print("Generating videos...")
for stream_type in streams:
    # Get the stream info and the cache; sort that frame cache based on frame number
    stream = streams[stream_type]
    s_frames_cache = sorted(stream['frames_cache'], key=lambda x: x[0])
    temp_dir = stream['temp_dir']

    # Generate an output video filename
    output_filename = os.path.join(dirname, filename+"_"+stream_type.split(".")[1]+".mp4")

    # Generate a video writer
    video_writer = cv2.VideoWriter(
        output_filename, 
        cv2.VideoWriter_fourcc(*'MP4V'), 
        args.output_dims[2], 
        [args.output_dims[0], args.output_dims[1]]
    )

    # Iterate through sorted frames
    for frame in s_frames_cache:
        img = cv2.imread(frame[1])
        if img is None:
            print(f"ERROR: Couldn't read image {frame[0]}")
            continue
        video_writer.write(img)

    # Release writer
    video_writer.release()

    # Delete temp folder
    shutil.rmtree(temp_dir)

    # Print results
    print(f"\tOutput stream {output_filename} generated from {stream_type}!")

print("Done: All streams outputted!")