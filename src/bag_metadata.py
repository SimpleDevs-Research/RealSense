import argparse
import os
import json
import pyrealsense2 as rs

parser = argparse.ArgumentParser(
    description="Read a `.bag` file to interpret its metadata. \
                Use to interpret what kind of streams the bag file contains.")
parser.add_argument("input", 
                    type=str, 
                    help="Path to the bag file")
parser.add_argument("-oj", "--output_json", 
                    action='store_true',  
                    help="Output stream params as a json file in the same location as the bag file")
args = parser.parse_args()

# Check if provided file actually exists
assert os.path.exists(args.input), "Input .bag file not detected."

# Generate an output for saving, in case we want to output all metadata into a json file
output = []

# Initialize a pipeline to read the bag file
pipeline = rs.pipeline()
config = rs.config()
config.enable_device_from_file(args.input, repeat_playback=False)

# Read the streams, output what kind of stream types they each are
profile = pipeline.start(config)

print("Streams found:")
for s in profile.get_streams():
    v = s.as_video_stream_profile()
    stream_type = str(s.stream_type())
    width = v.width()
    height = v.height()
    fps = v.fps()
    stream_format = str(v.format()) 
    output.append({'type':stream_type, 'format':stream_format, 'width':width, 'height':height, 'fps':fps})
    print(
        f"- TYPE: {stream_type}\t\t",
        f"RES: {width}x{height} @ {fps} FPS\t\t",
        f"FORMAT: {stream_format}"
    )

# Terminate the pipeline
pipeline.stop()

# If we want to save the outputs, save in the same location as the bag data
if args.output_json:
    # Determine the output save directory and file name
    filename_root, file_extension = os.path.splitext(args.input)
    dirname = os.path.dirname(filename_root)
    filename = os.path.basename(filename_root) 
    output_filename = os.path.join(dirname, filename+".json")

    # Prep and write output
    with open(output_filename, 'w') as outfile:
        json.dump(output, outfile, indent=2)
    print(f"Metadata outputted to `{output_filename}`")

