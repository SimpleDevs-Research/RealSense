import cv2
import numpy as np
import os
import time
from datetime import datetime
import json
import queue
import threading
import argparse
import pyrealsense2 as rs
from pynput import keyboard

# ================== #
# = PRIMITIVES = #
# ================== #

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


# ================== #
# SHARED STATE
# ================== #

latest_frame = None     # What's the latest updated frame?
frame_lock = threading.Lock()
event_queue = queue.Queue()
timestamps = []

stop_event = threading.Event()


# ========================= #
# = KEYBOARD PRESS THREAD = #
# ========================= #

def on_press(key):
    try:
        if key.char == ' ':
            event_queue.put('SPACE')
    except AttributeError:
        if key == keyboard.Key.space:
            event_queue.put('SPACE')
        elif key == keyboard.Key.esc:
            stop_event.set()
            return False


# ================== #
# = PREVIEW THREAD = #
# ================== #

def preview_loop():
    # Acecss the latest frame in this thread
    global latest_frame

    # Create the preview window
    cv2.namedWindow("Preview", cv2.WINDOW_AUTOSIZE)

    # Until the stop event runs, keep looping
    while not stop_event.is_set():
        frame = None

        # Copy the latest available frame
        with frame_lock:
            if latest_frame is not None:
                frame = latest_frame.copy()
        
        # Render the frame if it is not None
        if frame is not None:
            cv2.imshow("Preview", frame)
            cv2.waitKey(1)
        
        """
        # Key registration for spacebar
        key = cv2.waitKey(1) & 0xFF
        if key == 32:
            event_queue.put("SPACE")

        # key registration for closing the window
        if key == 27:
            stop_event.set()
            break
        """
    
    # Destroy the window
    cv2.destroyAllWindows()


# ==================== #
# = RECORDING THREAD = #
# ==================== #

def record_with_preview(metadata_path, output_dir, enable_preview):

    # Access the global frame
    global latest_frame

    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)

    # Form the output_path from metadata filename and current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{timestamp}.bag"
    output_path = os.path.join(args.output_dir, output_filename)

    # Initialize realsense pipeline
    pipeline = rs.pipeline()
    config = rs.config()

    # Load 
    is_color_frame = False
    with open(metadata_path, "r") as f:
        streams_raw = json.load(f)
        for stream in streams_raw:
            rs_type = _STREAM_TYPES[stream['type']]
            rs_format = _STREAM_FORMATS[stream['format']]
            config.enable_stream(rs_type, stream['width'], stream['height'], rs_format, stream['fps'])
            if stream['type'] == 'stream.color':
                is_color_frame = True
            print(f"Adding stream {stream['type']} as dictated via command arguments")
            

    # Configure output to specific `.bag` file
    config.enable_record_to_file(output_path)

    # Start recording
    pipeline.start(config)
    start_time = time.time()

    # Start listener for keyboardp resses
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.daemon = True
    keyboard_listener.start()

    # Start preview thread and window
    if enable_preview:
        preview_thread = threading.Thread(target=preview_loop, daemon=True)
        preview_thread.start()
    else:
        preview_thread = None
    print(f"Recording... Press ESC. to stop, SPACEBAR to mark timestamps")

    # Continue recording until stop event is reached
    try:
        while not stop_event.is_set():
            # Extract frame
            frames = pipeline.wait_for_frames()
            frame = frames.get_color_frame() if is_color_frame else frames.get_depth_frame()

            # handle if frame is not None
            if enable_preview and frame is not None:
                img = np.asarray(frame.get_data())
                # Copy latest frame for preview
                with frame_lock:
                    latest_frame = img.copy()
            
            # Check if preview thread sent spacebar event
            while not event_queue.empty():
                event = event_queue.get()
                if event == "SPACE":
                    timestamp = time.time() - start_time
                    timestamps.append(timestamp)
                    print(f"[MARK] {timestamp:.3f}s")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:

        # Stop everything
        stop_event.set()
        pipeline.stop()
        if preview_thread is not None:
            preview_thread.join()
        keyboard_listener.stop()

        # Save the timestamps too
        json_path = output_path.replace(".bag", "_timestamps.json")
        with open(json_path, "w") as f:
            json.dump(timestamps, f, indent=2)

        # Print messages
        print(f"Saved .bag to {output_path}")
        print(f"Saved timestamps to {json_path}")
        print("Timestamps:", timestamps)


# ================= #
# = EXAMPLE USAGE = #
# ================= #

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_metadata", 
                        type=str, 
                        help="The .json file to read")
    parser.add_argument("output_dir", 
                        type=str, 
                        help="The directory where the output bag is saved inside")
    parser.add_argument("-p", "--preview",
                        action="store_true",
                        help="Enable live OpenCV preview window")

    args = parser.parse_args()

    # double-check if input_metadata is a valid file
    assert os.path.exists(args.input_metadata), "Metadata file does not exists!"

    # Make the cal
    record_with_preview(args.input_metadata, args.output_dir, args.preview)



