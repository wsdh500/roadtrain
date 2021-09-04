
"""
Code for handling the Intel RealSense Depth Camera.
---------------------------------------------------
"""

import cv2
import pyrealsense2.pyrealsense2 as rs
import numpy as np

import time
import multiprocessing


#: The temperature at which to warn about the projector temperature.
proj_warn_temp = 40
#: The temperature at which to warn about the Asic temperature.
asic_warn_temp = 45

#: [OpenCV Colour Mappings](https://docs.opencv.org/4.5.0/d3/d50/group__imgproc__colormap.html)
colour_map = cv2.COLORMAP_HOT

rs_alpha = 0.1
rs_width = 1280
rs_height = 720
rs_format = rs.format.z16       # fixed for depth
rs_fps = 30
#: The current configuration. Use `rs-enumerate-devices` for available settings.
rs_args = (rs_alpha,rs_width,rs_height,rs_format,rs_fps,)

def depthcam_stream(alpha,width,height,dc_format,fps):
    '''
    .. _depthcam_stream:

    :param alpha: The alpha threshold to use when colourising.
    :param width: The width, in pixels, of the depth stream to use.
    :param height: The height, in pixels, of the depth stream to use.
    :param dc_format: Format for the depth camera to use.
    :param fps: Average frames-per-second to capture with the depth camera.

    Creates a window and displays the depth stream within it.
    '''
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth,width,height,dc_format,fps)
    cfg = None
    try:
        cfg = pipeline.start(config)
    except RuntimeError:
        print('Intel RealSense Depth Camera not connected.')
        return
    device = cfg.get_device()
    first_depth_sensor = device.first_depth_sensor()
    rs_window = 'RealSense'
    cv2.namedWindow(rs_window,cv2.WINDOW_AUTOSIZE|cv2.WINDOW_GUI_NORMAL)
    RUNNING=True
    try:
        while RUNNING:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                print('Not depth frame, skipping ...')
                continue
            depth_image = np.asanyarray(depth_frame.get_data())
            converted = cv2.convertScaleAbs(depth_image,alpha=alpha) # matrix of normalised bytes in range [0,255]
            depth_colormap = cv2.applyColorMap(converted,colour_map) # matrix of 3 byte arrays representing RGB.
            cv2.imshow(rs_window,depth_colormap)
            cv2.setWindowProperty(rs_window,cv2.WND_PROP_TOPMOST,1)
            cv2.waitKey(1)
            if cv2.getWindowProperty(rs_window,cv2.WND_PROP_VISIBLE) < 1:
                RUNNING = False
            temp = first_depth_sensor.get_option(rs.option.projector_temperature)
            if temp > proj_warn_temp:
                print("Projector temperature too hot :",str(temp))
            temp = first_depth_sensor.get_option(rs.option.asic_temperature)
            if temp > asic_warn_temp:
                print("Asic temperature too hot :",str(temp))
    finally:
        print('Shutting down RealSense.')
        pipeline.stop()
        cv2.destroyWindow(rs_window)


def create_event_handlers(rs_args):
    '''
    :param rs_args: A tuple of arguments for :ref:`depthcam_stream <depthcam_stream>`.

    Creates a pair of event handlers :

    * One opens a window displaying the depth stream from the camera,
    * the other closes that window and shuts down the depth camera.

    '''
    rs_process = None
    last_event = 0

    def activate_event():
        nonlocal rs_process
        nonlocal last_event
        if rs_process == None and time.time() - last_event > 0.5:
            last_event = time.time()
            rs_process = multiprocessing.Process(target=depthcam_stream,args=rs_args)
            rs_process.start()

    def terminate_event():
        nonlocal rs_process
        nonlocal last_event
        if rs_process != None and time.time() - last_event > 1.5:
            last_event = time.time()
            rs_process.terminate()
            rs_process = None

    return activate_event , terminate_event


if __name__ == "__main__":

    activate , terminate = create_event_handlers(rs_args)
    activate()
