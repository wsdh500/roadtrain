
"""
Code for handling the Intel RealSense Depth Camera.
---------------------------------------------------

Please see ``/usr/local/bin/rs-enumerate-devices``
for compatible depth camera stream arguments.
"""

import cv2
import pyrealsense2.pyrealsense2 as rs
import numpy as np

import time
import multiprocessing


#: The temperature at which to warn about the projector, or the Asic, temperature.
warn_temp = 40
#: The temperature at which to shutdown the RealSense camera.
shutdown_temp = 45

rs_window = 'RealSense'

default_map = cv2.COLORMAP_HOT

def check_temperature(depth_sensor):
    '''
    :param depth_sensor: Depth Camera to be checked.

    Checks the projector, and the Asic, temperatures to see if the depth camera is overheating.

    :return: boolean indicating whether the camera is overheating.
    '''
    OK = True
    proj_temp = depth_sensor.get_option(rs.option.projector_temperature)
    asic_temp = depth_sensor.get_option(rs.option.asic_temperature)
    max_temp = max(proj_temp,asic_temp)
    if max_temp > warn_temp:
        print("RealSense temperature too hot",str(temp),'degrees.')
    if max_temp > shutdown_temp:
        print("RealSense shuting down to prevent overheating",str(temp),'degrees.')
        OK = False
    return OK


def depth_stream(colour_map,scale_factor=0.1,width=1280,height=720,fps=30):
    '''
    .. _depth_stream:

    :param color_map: OpenCV colour mapping.
    :param scale_factor: Depth scaling factor to use.
    :param width: The width, in pixels, of the depth stream to use.
    :param height: The height, in pixels, of the depth stream to use.
    :param fps: Average frames-per-second to capture with the depth camera.

    Creates a window and displays the depth stream within it.

    see : `OpenCV colour mappings <https://docs.opencv.org/4.5.0/d3/d50/group__imgproc__colormap.html>`_
    '''
    if colour_map == None:
        colour_map = default_map
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth,width,height,rs.format.z16,fps)
    cfg = None
    try:
        cfg = pipeline.start(config)
    except RuntimeError:
        print('Intel RealSense Depth Camera not connected.')
        return
    device = cfg.get_device()
    first_depth_sensor = device.first_depth_sensor()
    cv2.namedWindow(rs_window,cv2.WINDOW_AUTOSIZE|cv2.WINDOW_GUI_NORMAL)
    RUNNING=True
    try:
        while RUNNING:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                print('Not depth frame, skipping ...')
                continue
            depth = np.asanyarray(depth_frame.get_data())
            scaled = cv2.convertScaleAbs(depth,alpha=scale_factor) # matrix of normalised bytes in range [0,255]
            colormapped = cv2.applyColorMap(scaled,colour_map) # matrix of 3 byte arrays representing RGB.
            cv2.imshow(rs_window,colormapped)
            cv2.setWindowProperty(rs_window,cv2.WND_PROP_TOPMOST,1)
            cv2.waitKey(1)
            if cv2.getWindowProperty(rs_window,cv2.WND_PROP_VISIBLE) < 1:
                RUNNING = False

            RUNNING &= check_temperature(first_depth_sensor)

    finally:
        print('Shutting down RealSense.')
        pipeline.stop()
        cv2.destroyWindow(rs_window)
    return

def combined_stream(colour_map,scale_factor=0.1,alpha=0.6,width=640,height=480,fps=60):
    '''
    .. _combined_stream:

    :param color_map: OpenCV colour mapping.
    :param scale_factor: Depth scaling factor to use.
    :param alpha: Transparancy value to use when blending streams.
    :param width: The width, in pixels, of the combined streams to use.
    :param height: The height, in pixels, of the combined streams to use.
    :param fps: Average frames-per-second to capture both depth camera streams.

    Creates a window and displays a blend of the video and depth streams within it.

    see : `OpenCV colour mappings <https://docs.opencv.org/4.5.0/d3/d50/group__imgproc__colormap.html>`_
    '''
    if colour_map == None:
        colour_map = default_map

    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth,width,height,rs.format.z16,fps)
    config.enable_stream(rs.stream.color,width,height,rs.format.bgr8,fps)
    align = rs.align(rs.stream.color)

    cfg = None
    try:
        cfg = pipeline.start(config)
    except RuntimeError:
        print('Intel RealSense Depth Camera not connected.')
        return

    device = cfg.get_device()
    first_depth_sensor = device.first_depth_sensor()

    cv2.namedWindow(rs_window,cv2.WINDOW_AUTOSIZE|cv2.WINDOW_GUI_NORMAL)
    cv2.moveWindow(rs_window,32,32)

    RUNNING=True
    try:
        while RUNNING:
            frames = pipeline.wait_for_frames()
            frames = align.process(frames)

            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                continue

            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            depth_frame.keep() # ??
            depth = np.asanyarray(depth_frame.get_data())
            scaled = cv2.convertScaleAbs(depth,alpha=scale_factor) # matrix of normalised bytes in range [0,255]
            colormapped = cv2.applyColorMap(scaled,colour_map) # matrix of 3 byte arrays representing RGB.

            color_frame.keep() # ???
            image = np.asanyarray(color_frame.get_data())

            blended = cv2.addWeighted(colormapped,alpha,image,1.0-alpha,0.0)

            cv2.imshow(rs_window,blended)
            cv2.setWindowProperty(rs_window,cv2.WND_PROP_TOPMOST,1)
            cv2.waitKey(1)
            if cv2.getWindowProperty(rs_window,cv2.WND_PROP_VISIBLE) < 1:
                RUNNING = False

            RUNNING &= check_temperature(first_depth_sensor)

    finally:
        pipeline.stop()
        cv2.destroyWindow(rs_window)
    return


def create_event_handlers(stream,args):
    '''
    :param stream: A stream function to execute in (depth_strea,combined_stream).
    :param args: A tuple of arguments for the stream.

    Creates a pair of event handlers :

    * One opens a window displaying the stream from the depth camera,
    * the other closes that window and shuts down the depth camera.

    :ref:`depth_stream <depth_stream>`,
    :ref:`combined_stream <combined_stream>`.

    '''
    rs_process = None
    last_event = 0

    def activate_event():
        nonlocal rs_process
        nonlocal last_event
        if rs_process == None and time.time() - last_event > 0.5:
            last_event = time.time()
            rs_process = multiprocessing.Process(target=stream,args=args)
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

    args = (cv2.COLORMAP_HOT,)
    activate , terminate = create_event_handlers(depth_stream,args)
    activate()
