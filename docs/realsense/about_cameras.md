# About Realsense Cameras

Intel Realsense is a division within the Intel company that releases camera hardware and software. The ones we typically deal with are of **two** types:

|Type|Description|Intel Classification|
|:-:|:--|:--|
|**RGB-D Cameras**|Depth is perceived from _stereoscopic_ cameras: two separate cameras looking at the same scene, but slightly off-kilter from each other. Depth is perceived from the differences between the two scenes at a pixel level.|`D400`|
|**LiDAR Cameras**|Depth is perceived from the implementation of _LiDAR_, or "Light Detection and Ranging". In essence, one or more lasers are shot out, reflected off of surfaces, and are sensed by the LiDAR device. The sensor uses the time-of-flight of these lasers to estimate depth.|`L500` (Discontinued)|

At the SimSpace Laboratory, you have access to **two** cameras: the [_D435i_](https://realsenseai.com/products/depth-camera-d435i/) and the [_L515_](https://www.amazon.com/Intel-RealSense-Camera-Logistics-Industry/dp/B0BJ5S2D4R).

## Which Do I Use?

Your mileage will vary depending on the task.

- Stereoscopic Depth cameras are generally less accurate and don't _truly_ sense depth. This means that visual illusions and occlusions will trick the depth perception of these cameras. All other factors that normal cameras face will also affect these kinds of cameras, such as ambient light, fog, etc.
- LiDAR cameras don't face the same struggles as stereoscopic depth cameras because LiDAR is a _laser_-based system. That being said, depending on the build quality of your LiDAR, its accuracy may be varied. LiDAR cameras also are massive power hogs!

Among the **D435i** and **L515**, we generally recommend the **D435i** despite its issues. This is because the **L515** does not see as far as the **D435i** and requires a lot of power; this makes it untenable as a useful device.