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

depth_format_map = {
    'z16':rs.format.z16
}
color_format_map = {
    'rgb8': rs.format.rgb8,
    'bgr8': rs.format.bgr8,
    'yuyv': rs.format.yuyv
}

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("input", 
                    type=str, 
                    help="The local path to the bag file")
parser.add_argument('-d', '--depth', 
                    action='store_true', 
                    help='Process and render the depth data from the input file')
parser.add_argument('-c', '--color', 
                    action='store_true', 
                    help='Process and render the color data from the input file')
parser.add_argument("-dr", "--depth_resolution", 
                    nargs=2, 
                    default=[640, 480], 
                    type=int, 
                    help="The resolution of the depth video")
parser.add_argument("-cr", "--color_resolution", 
                    nargs=2, 
                    default=[640, 480], 
                    type=int, 
                    help="The resolution of the color video")
parser.add_argument("-dfps", "--depth_fps", 
                    type=int, 
                    default=15, 
                    help="The FPS of the depth video")
parser.add_argument("-cfps", "--color_fps", 
                    type=int, 
                    default=15, 
                    help="The FPS of the color video")
parser.add_argument("-df", "--depth_format", 
                    type=str, 
                    default='z16', 
                    choices={'z16'}, 
                    help="The depth format of the video (default='z16')")
parser.add_argument("-cf", "--color_format", 
                    type=str, 
                    default='bgr8', 
                    choices={'bgr8', 'rgb8', 'yuyv'}, 
                    help="The color mode of the video (default='bgr8')")
parser.add_argument("-o", "--output", 
                    action='store_true', 
                    help="Should we print out a vidoe file?")
parser.add_argument("-or", "--output_resolution", 
                    nargs=2, 
                    default=[640, 480], 
                    type=int, 
                    help="The output video resolution. Provide values for the frame size of a single stream (depth or color); images will be resized based on if a single image or both the depth and color are added.")
parser.add_argument("-ofps", '--output_fps', 
                    default=15, 
                    type=int, 
                    help="The output FPS of the video. Please ensure that this is equivalent to the depth, color, or both.")
parser.add_argument("-so", "--show_output",
                    action='store_true'
                    help="Should we output the streams into a pythn window for viewing? WILL CAUSE LAG!")

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
# Check that we're processing at least either depth or color
if not args.depth and not args.color:
    print("ERROR: Neither depth or color was selected for render")
    exit()

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, args.input)

    # Interpret the depth and color modes from the user's input, or go with default Z16 and BGR8
    depth_format = depth_format_map[args.depth_format]
    color_format = color_format_map[args.color_format]

    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    if args.depth: 
        config.enable_stream(rs.stream.depth, args.depth_resolution[0], args.depth_resolution[1], depth_format, args.depth_fps)
    if args.color:
        config.enable_stream(rs.stream.color, args.color_resolution[0], args.color_resolution[1], color_format, args.color_fps)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    if args.show_output: 
        cv2.namedWindow("Depth and Color Stream", cv2.WINDOW_AUTOSIZE)

    if args.output:
        base = os.path.basename(args.input)
        filename = os.path.splitext(base)[0]
        output_dir = os.path.dirname(args.input)
        output_path = os.path.join(output_dir, filename+".mp4")
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out_res = [args.output_resolution[0], args.output_resolution[1]]
        if args.depth and args.color: out_res[0] = args.output_resolution[0] * 2
        out = cv2.VideoWriter(output_path, fourcc, args.output_fps, out_res)
    else:
        out = None
    
    # Create colorizer object
    colorizer = rs.colorizer()

    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get the depth frame and conduct processing
        if args.depth:
            # Get frame
            depth_frame = frames.get_depth_frame()
            # Colorize depth frame to jet colormap
            depth_color_frame = colorizer.colorize(depth_frame)
            # Convert depth_color_frame to numpy array to render image in opencv
            depth_image = np.asanyarray(depth_color_frame.get_data())
            # Get the dimensions of the depth frame
            depth_colormap_dim = depth_image.shape

        if args.color:
            # Get frame
            color_frame = frames.get_color_frame()
            # Convert color_frame to numpy array to render image in opencv
            color_image = np.asanyarray(color_frame.get_data())
            # Get the dimensions of the color frame
            color_colormap_dim = color_image.shape

        # If we have BOTH depth and color frame, we have to resize the images so that they're the same size
        # Specifically, if depth and color resolutions are different, resize color image to match depth image for display
        if args.depth and args.color:
            if depth_colormap_dim != color_colormap_dim[0:1]:
                resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
                images = np.hstack((resized_color_image, depth_image))
            else:
                images = np.hstack((color_image, depth_image))
        elif args.depth:
            images = depth_image
        elif args.color:
            images = color_image

        # Render image in opencv window
        if args.show_output:
            cv2.imshow("Depth and Color Stream", images)
        # Write an output to the output video if there is an output stream set up
        if out is not None:
            images = cv2.resize(images, out_res, interpolation = cv2.INTER_CUBIC)
            out.write(images)
        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            out.release()
            break

finally:
    pass
