import argparse
import numpy as np
import cv2
import os
import json
from scipy.io import savemat, loadmat
import shutil
import gc
import pyrealsense2 as rs
from tqdm import tqdm

# Custom import script
import helpers

# ======================================
# ===== STREAM CLASS ===================
# ======================================

class Stream:
    def __init__(self, name:str, data_dir:str, width:int, height:int, fps:int):
        self.name = name
        self.data_dir = helpers.mkdirs(data_dir)
        self.frames = []
        self.width = width
        self.height = height
        self.fps = fps

    def add_frame(self, fn:int, ts:float, frame):
        out_filename = os.path.join(self.data_dir, f"{fn}.png")
        cv2.imwrite(out_filename, frame)
        self.frames.append([fn, ts, out_filename])
        return self

    def add_mat(self, fn:int, ts:float, frame, depth_scale:float, depth_intrinsics):
        out_filename = os.path.join(self.data_dir, f"{fn}.mat")
        savemat(out_filename, { 
            'depth':frame, 
            'frame_number':fn, 
            'timestamp':ts, 
            'depth_scale':depth_scale,
            "width": depth_intrinsics.width,
            "height": depth_intrinsics.height,
            "fx": depth_intrinsics.fx,
            "fy": depth_intrinsics.fy,
            "cx": depth_intrinsics.ppx,
            "cy": depth_intrinsics.ppy
        })
        self.frames.append([fn, ts, out_filename])
        return self
    
    def sort_frames(self):
        sorted_frames = sorted(self.frames, key=lambda x: x[1])
        self.frames = sorted_frames
        return self

    def generate_video(self):

        # Initialize the writer and other variables
        out_filename = self.name+'.mp4'
        writer = cv2.VideoWriter( out_filename, cv2.VideoWriter_fourcc(*'MP4V'), self.fps, [self.width, self.height])
        prev_ts = None
        frame_time = 1000 / self.fps
        print(f"Starting to generate video \"{out_filename}\"...")

        # Iterate through frames
        for i in tqdm(range(len(self.frames))):
            frame = self.frames[i]
            img = cv2.imread(frame[2])
            if img is None:
                print(f"ERROR: Couldn't read image {frame[0]}")
                continue
            # if there's no previous timestamp, then we just add the image itself and set `prev_ts`
            if prev_ts is None:
                writer.write(img)
                prev_ts = frame[1]
                continue;
            # Calcualte delta time
            dt = frame[1] - prev_ts
            prev_ts = frame[1]
            # Consecutively add frames until the next active frame
            frames_to_write = max(1, round(dt / frame_time))
            for _ in range(frames_to_write):
                writer.write(img)

        # At the end, report results, close the writer, and return self
        print(f"\tOutput stream {out_filename} generated!")
        writer.release()
        return self
    
    def generate_allmat(self):
        # Initialize the variables
        out_filename = self.name+'.mat'
        depths = []
        timestamps = []
        frame_numbers = []
        depth_scales = []
        widths = []
        heights = []
        fxs = []
        fys = []
        cxs = []
        cys = []
        print(f"Starting to aggregate materials for {out_filename}...")

        # Iterate through frames
        for i in tqdm(range(len(self.frames))):
            frame = self.frames[i]
            data = loadmat(frame[2])
            if data is None:
                print(f"ERROR: Couldn't read material @ {frame[0]}")
                continue
            # Get our depth data
            depths.append(data["depth"])
            frame_numbers.append(data["frame_number"][0][0])
            timestamps.append(data["timestamp"][0][0])
            depth_scales.append(data['depth_scale'][0][0])
            widths.append(data['width'][0][0])
            heights.append(data['height'][0][0])
            fxs.append(data['fx'][0][0])
            fys.append(data['fy'][0][0])
            cxs.append(data['cx'][0][0])
            cys.append(data['cy'][0][0])
            
        # Now combine everything into a singular output
        print(f"Combining aggregations into single material {out_filename}...")
        savemat(out_filename, {
            "depth_frames": np.stack(depths, axis=0),
            "timestamps": np.array(timestamps),
            "frame_numbers": np.array(frame_numbers),
            "depth_scales": np.array(depth_scales),
            "widths": np.array(widths),
            "heights": np.array(heights),
            "fxs": np.array(fxs),
            "fys": np.array(fys),
            "cxs": np.array(cxs),
            "cys": np.array(cys)
        })

        # At the end, report output and return self
        print(f"\tOutput material {out_filename} generated!")
        return self
    
    def delete_data_dir(self):
        shutil.rmtree(self.data_dir)
        return self


# ======================================
# ===== MAIN FUNCTION ==================
# ======================================


# Define our main key functio: extract_from_bag()
def extract_from_bag(input_bag:str, input_metadata:str):

    # Check if provided files actually exist
    assert os.path.exists(input_bag), "Input .bag file not detected."
    assert os.path.exists(input_metadata), "Input .json metadata file not detected"
    
    # ======================================
    # ===== INITIALIZATIONS ================
    # ======================================

    # Remove the `.bag` from `input_bag`
    root, ext = os.path.splitext(input_bag)

    # Initialize OpenCV writers and other arrays
    color_stream = None
    depth_stream = None
    raw_depth_stream = None

    # Initialize librealsense
    pipeline = rs.pipeline()
    config = rs.config()
    depth_intrinsices = None
    profile = None

    # ======================================
    # ===== CONFIGURATIONS =================
    # ======================================

    # Connect input bag data to rs.config
    config.enable_device_from_file(input_bag, repeat_playback=False)

    # Read the input metadata, enable their streams
    with open(args.input_metadata, "r") as f:
        streams_raw = json.load(f)      # Load from JSON
        for stream in streams_raw:      # Loop through raw stream meta
            
            rs_type = helpers._STREAM_TYPES[stream['type']]         # Convert stream type
            rs_format = helpers._STREAM_FORMATS[stream['format']]   # Convert stream format
            
            # Enable the stream via config
            config.enable_stream( rs_type, stream['width'], stream['height'], rs_format, stream['fps'] )

            # Initialize streams for each color, depth, and raw depth data
            if stream['type'] == 'stream.color':
                color_stream = Stream(root+"_color", root+"_color", stream['width'], stream['height'], stream['fps'])
            elif stream['type'] == 'stream.depth':
                depth_stream = Stream(root+"_depth", root+"_depth", stream['width'], stream['height'], stream['fps'])
                raw_depth_stream = Stream(root+"_depth", root+"_raw_depth", stream['width'], stream['height'], stream['fps'])

    # Consider the case that no streams were considred
    assert color_stream is not None or depth_stream is not None, "No streams are set for being outputted..."

    # Initialize Frame Aligner, for aligning frames. We force the frames to align to the RGB component if it exists; otherwise, use the first stream in `streams`
    align_to = rs.stream.color if color_stream is not None else rs.stream.depth
    frame_aligner = rs.align(align_to)

    # Initialize a colorizer to visualize the depth color
    frame_colorizer = rs.colorizer()

    # =====================================
    # ===== READ BAG DATA =================
    # =====================================

    try:
        # Read the streams, output what kind of stream types they each are
        profile = pipeline.start(config)
        playback = profile.get_device().as_playback()
        playback.set_real_time(False)

        # Interpret depth scale
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)

        # Start iterating through frames
        print("Reading `.bag` data...")
        while True:
            # Wait for frames, pause playback. If frames don't exist anymore, exit early
            frame_present, frames = pipeline.try_wait_for_frames()
            playback.pause()
            if not frame_present:
                print("Frames no longer present!")
                break

            # Apply alignment
            aligned_frames = frame_aligner.process(frames)

            # Try and get color frame
            if color_stream is not None: 
                frame = aligned_frames.get_color_frame()
                ts = frame.get_timestamp()
                fn = frame.get_frame_number()
                # Handle color image
                color_stream.add_frame(fn, ts, np.asanyarray(frame.get_data()))
            
            # Try and get depth frame
            if depth_stream is not None:
                frame = aligned_frames.get_depth_frame()
                ts = frame.get_timestamp()
                fn = frame.get_frame_number()
                if depth_intrinsices is None: depth_intrinsices = frame.get_profile().as_video_stream_profile().get_intrinsics()
                # Handle colorized data first
                color_frame = frame_colorizer.colorize(frame)
                depth_stream.add_frame(fn, ts, np.asanyarray(color_frame.get_data()))
                # Now handle raw data
                raw_depth_stream.add_mat(fn, ts, np.asanyarray(frame.get_data()), depth_scale, depth_intrinsices)

            # If pressed ESC, exit reading the 
            key = cv2.waitKey(1) & 0xFF
            if key == 27: break

            # Resume playback
            playback.resume()
    
    # EXCEPTION! Something happened. Report via logs
    except Exception as e:
        print("ERROR: Reading bag ended due to exception catch")
        print(e)

    # Cleanup, concatenating all generated mat data, closing pipelines
    finally:
        # End pipeline
        if profile is not None: pipeline.stop()


    # =====================================
    # ===== GENERATE VIDEOS AND MAT =======
    # =====================================

    # We now need to handle each of the streams. Or try to, at least
    try:
        if color_stream is not None:
            if len(color_stream.frames) > 0: color_stream.sort_frames().generate_video()
            else: print("No color frames aggregate...")
        if depth_stream is not None:
            if len(depth_stream.frames) > 0: depth_stream.sort_frames().generate_video()
            else: print("No depth frames aggregated...")
        if raw_depth_stream is not None:
            if len(raw_depth_stream.frames) > 0: raw_depth_stream.sort_frames().generate_allmat()
            else: print("No depth materials aggregated...")
    except Exception as e:
        print("ERROR: Generating streams into videos and material stopped early")
        print(e)
    finally:
        if color_stream is not None:        color_stream.delete_data_dir()
        if depth_stream is not None:        depth_stream.delete_data_dir()
        if raw_depth_stream is not None:    raw_depth_stream.delete_data_dir()

    # Print out final results
    print("Done! Closing Generator!")



# ======================================
# ===== EXAMPLE ========================
# ======================================

if __name__ == "__main__":

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
    args = parser.parse_args()

    # Run our function
    extract_from_bag(args.input_bag, args.input_metadata)

