import os
import shutil
from random import choice
from string import ascii_uppercase
import pyrealsense2 as rs



# ===================================================================
# ===== MAPPERS, DICTIONARIES =======================================
# ===================================================================

# String to librealsense stream type
_STREAM_TYPES = {
    'stream.depth': rs.stream.depth,
    'stream.color': rs.stream.color
}

# String to librealsense stream format
_STREAM_FORMATS = {
    'format.z16': rs.format.z16,
    'format.rgb8': rs.format.rgb8,
    'format.bgr8': rs.format.bgr8,
    'format.yuyv': rs.format.yuyv
}



# ===================================================================
# ===== HELPER FUNCTIONS ============================================
# ===================================================================

# Forcefully create directories. We can control to delete existing directories if detected.
def mkdirs(query_dir:str, delete_existing:bool=True):
    if delete_existing and os.path.exists(query_dir): 
        shutil.rmtree(query_dir)            # If the folder already exists, delete it
    os.makedirs(query_dir, exist_ok=True)   # Create a new empty directory
    return query_dir                        # Return the directory to indicate completion

# Randomly generate strings of given length
def create_random_str(length:int = 12):
    return ''.join(choice(ascii_uppercase) for i in range(length))

# Create dictionaries with random string filenames
def create_random_dir(delete_existing:bool=True, append_tag:str=None):
    output_filename = create_random_str()
    if append_tag is not None: output_filename += append_tag
    return mkdirs(output_filename)
