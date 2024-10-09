#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-r", "--resolution", nargs='+', default=[], type=int, help="resolution of depth and color video")
parser.add_argument("-f", "--fps", nargs='+', default=[], type=int, help="frame rate of depth and color video")
parser.add_argument("-d", dest="depth", action="store_true", help="render depth video")
parser.add_argument("-c", dest="color", action="store_true", help="render color video")
parser.add_argument("-i", "--input", type=str, help="Path to the bag file")

parser.set_defaults(depth=False, color=False)
# Parse the command line arguments to an object
args = parser.parse_args()
# Safety if no parameter have been given
if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
# Check if the given file have bag extension
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()
try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, args.input)

    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    if (args.depth == True and args.color == True):
        config.enable_stream(rs.stream.depth, args.resolution[0], args.resolution[1], rs.format.z16, args.fps[0])
        config.enable_stream(rs.stream.color, args.resolution[2], args.resolution[3], rs.format.rgb8, args.fps[1])
        cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Color Stream", cv2.WINDOW_AUTOSIZE)
    
    elif (args.depth == True):
        config.enable_stream(rs.stream.depth, args.resolution[0], args.resolution[1], rs.format.z16, args.fps[0])
        cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    
    elif (args.color == True):
        config.enable_stream(rs.stream.color, args.resolution[0], args.resolution[1], rs.format.rgb8, args.fps[0])
        cv2.namedWindow("Color Stream", cv2.WINDOW_AUTOSIZE)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    
    
    # Create colorizer object
    colorizer = rs.colorizer()

    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get depth frame
        if (args.depth == True):
            depth_frame = frames.get_depth_frame()
            depth_color_frame = colorizer.colorize(depth_frame)
            depth_color_image = np.asanyarray(depth_color_frame.get_data())
            cv2.imshow("Depth Stream", depth_color_image)
        
        if (args.color == True):
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            cv2.imshow("Color Stream", color_image)
        
        
        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            break

finally:
    pass
