import argparse
import json
import pyrealsense2 as rs

# Parse arguments
parser = argparse.ArgumentParser(
    description="Using an attached Realsense camera and a configuration of your own, \
                record a `.bag` file via Python")
parser.add_argument("input_metadata",
                    type=str,
                    help="Path to the input metadata file to control the recording")
parser.add_argument("output_bag", 
                    type=str, 
                    help="Path to the outputted bag file")
parser.add_argument("-p", "--preview",
                    action="store_true",
                    help="Should a preview of what's written by shown? Don't include this command if you want to maximize recording sampling rate")
args = parser.parse_args()

# Initialize our realsense stuff
pipeline = rs.pipeline()
config = rs.config()

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
    for stream in streams_raw:
        rs_type = _STREAM_TYPES[stream['type']]
        rs_format = _STREAM_FORMATS[stream['format']]
        config.enable_stream(rs_type, stream['width'], stream['height'], rs_format, stream['fps'])
        print(f"Adding stream {stream['type']} as dictated via command arguments")

# Set the output bag
config.enable_record_to_file(args.output_bag)

# Start recording
pipeline.start(config)
print("Recording... Press Ctrl+C to stop.")

# Try, Except, and Finally
try:
    while True:
        frames = pipeline.wait_for_frames()
        pass
except KeyboardInterrupt:
    print("Stopping...")
finally:
    pipeline.stop()
    print(f"Saved to {args.output_bag}")
