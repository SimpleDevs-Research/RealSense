import scipy.io as sio
import numpy as np
import open3d as o3d
import time
import keyboard
import argparse

def render_3d_mat(input_mat:str):
    mat = sio.loadmat(input_mat)
    depth_frames = mat["depth_frames"]     # uint16, shape (N,H,W)
    timestamps   = mat["timestamps"].flatten()
    frame_numbers = mat["frame_numbers"].flatten()

    # Per-frame intrinsics (adjust keys as needed)
    widths = mat['widths'].flatten()
    heights = mat['heights'].flatten()
    fxs = mat["fxs"].flatten()
    fys = mat["fys"].flatten()
    cxs = mat["cxs"].flatten()
    cys = mat["cys"].flatten()
    scales = mat["depth_scales"].flatten()   # e.g. mm -> meters

    N, H, W = depth_frames.shape

    # -----------------------------------------------------
    # Convert a depth frame to a point cloud using that frame's intrinsics
    # -----------------------------------------------------
    def depth_to_pcd(depth, fx, fy, cx, cy, scale):
        z = depth.astype(np.float32) * scale
        u, v = np.meshgrid(np.arange(W), np.arange(H))

        x = (u - cx) * z / fx
        y = (v - cy) * z / fy

        pts = np.stack((x, -y, z), axis=-1).reshape(-1, 3)

        # Remove invalid (zero) depth points
        mask = pts[:, 2] > 0
        pts = pts[mask]

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pts)
        return pcd

    # -----------------------------------------------------
    # Initialize Open3D visualizer
    # -----------------------------------------------------
    frame_idx = 0

    pcd = depth_to_pcd(
        depth_frames[frame_idx],
        fxs[frame_idx], fys[frame_idx],
        cxs[frame_idx], cys[frame_idx],
        scales[frame_idx]
    )

    vis = o3d.visualization.Visualizer()
    vis.create_window("3D Depth Player", width=max(widths), height=max(heights))
    vis.add_geometry(pcd)

    is_playing = True
    fps = 30
    frame_interval = 1.0 / fps
    last_time = time.time()

    print("3D Depth Player Loaded!")
    print("Controls:")
    print("  SPACE = Play/Pause")
    print("  →     = Next Frame")
    print("  ←     = Previous Frame")
    print("Close the window to exit.")


    # -----------------------------------------------------
    # Playback Loop
    # -----------------------------------------------------
    while True:

        # Keyboard controls
        if keyboard.is_pressed("right"):
            frame_idx = (frame_idx + 1) % N
            time.sleep(0.15)

        if keyboard.is_pressed("left"):
            frame_idx = (frame_idx - 1) % N
            time.sleep(0.15)

        if keyboard.is_pressed("space"):
            print("Changing is_playing")
            is_playing = not is_playing
            print("Changed is_playing")
            time.sleep(0.25)

        # Auto-play mode
        if is_playing:
            now = time.time()
            if now - last_time > frame_interval:
                frame_idx = (frame_idx + 1) % N
                last_time = now

        # Update point cloud with correct intrinsics
        depth = depth_frames[frame_idx]

        pcd_new = depth_to_pcd(
            depth,
            fxs[frame_idx], fys[frame_idx],
            cxs[frame_idx], cys[frame_idx],
            scales[frame_idx]
        )
        pcd.points = pcd_new.points

        vis.update_geometry(pcd)

        if not vis.poll_events():
            break

        vis.update_renderer()
        time.sleep(0.01)

    vis.destroy_window()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Render 3D mat data")
    parser.add_argument('input_mat', type=str, help="The input material to render")
    args = parser.parse_args()

    render_3d_mat(args.input_mat)