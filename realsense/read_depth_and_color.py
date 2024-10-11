################################################################################
##               Read both depth and color video from bag file                ##
################################################################################


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
parser.add_argument("input", type=str, help="local path to the bag file")
#parser.add_argument("depth_resolution", nargs='2', default=[640, 480], type=int, help="Resolution of the depth video")
#parser.add_argument("color_resolution", nargs='2', default=[640, 480], type=int, help="Resolution of the color video")
parser.add_argument("depth_fps", type=int, help="the FPS of the depth video")
parser.add_argument("color_fps", type=int, help="the FPS of the color video")
parser.add_argument("-cf", "--color_format", type=str, help="the color mode of the video (Default='bgr8')", default='bgr8', choices={'bgr8', 'rgb8'})
parser.add_argument("-o", "--output", action='store_true', help="Should we print out a vidoe file?")

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

    # Interpret the color mode from the user's input, or go with default BGR8
    if args.color_format == 'rgb8':
        color_format = rs.format.rgb8
    else:
        color_format = rs.format.bgr8

    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    config.enable_stream(rs.stream.depth, rs.format.z16, args.depth_fps)
    config.enable_stream(rs.stream.color, color_format, args.color_fps)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    cv2.namedWindow("Depth and Color Stream", cv2.WINDOW_AUTOSIZE)

    if args.output:
        base = os.path.basename(args.input)
        filename = os.path.splitext(base)[0]
        output_dir = os.path.dirname(args.input)
        output_path = os.path.join(output_dir, filename+".mp4")
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter(output_path, fourcc, 15.0, (640*2,480))
    else:
        out = None
    
    # Create colorizer object
    colorizer = rs.colorizer()

    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get depth frame
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # Colorize depth frame to jet colormap
        depth_color_frame = colorizer.colorize(depth_frame)

        # Convert depth_frame and color_frame to numpy array to render image in opencv
        depth_image = np.asanyarray(depth_color_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Get the dimensions of the depth and color frames
        depth_colormap_dim = depth_image.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_image))
        else:
            images = np.hstack((color_image, depth_image))

        # Render image in opencv window
        cv2.imshow("Depth and Color Stream", images)
        if out is not None:
            out.write(images)
        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            out.release()
            break

finally:
    pass
