import pyrealsense2 as rs

ctx = rs.context()
devices = ctx.query_devices()

if len(devices) == 0:
    print("No RealSense devices connected.")
else:
    print("Connected devices:")
    for dev in devices:
        print(" -", dev.get_info(rs.camera_info.name))
        print("   Serial:", dev.get_info(rs.camera_info.serial_number))