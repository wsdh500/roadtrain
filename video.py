
import cv2
from display import n_displays , x_offset , y_offset
from sys import exit

import time

n = n_displays()


def create_offset():
    offset = 0
    last_event = 0

    def increment():
        nonlocal offset
        nonlocal last_event
        if time.time() - last_event > 0.3:
            offset += n
            last_event = time.time()

    def current():
        nonlocal offset
        return offset

    return increment , current

increment_offset , current_offset = create_offset()

def get_switcher():
    return increment_offset


QUIT_KEY = ord('q')
NEXT_KEY = ord('n')

caps = []
windows = []

INITIALISED = False

def open_stream(stream):
    cap = cv2.VideoCapture(stream)
    if(cap.isOpened() == False):
        print('Cannot open stream',str(stream))
        exit()
    return cap

def open_window(window_name,x_offset,y_offset,full_screen):
    if full_screen:
        cv2.namedWindow(window_name,cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(window_name,x_offset,y_offset)
    return window_name

def setup_window(path,window_name,x_offset,y_offset,full_screen):
    cap = open_stream(path)
    video_window = open_window(window_name,x_offset,y_offset,full_screen)
    return cap , video_window

def video_setup(paths,full_screen):
    for path in paths:
        cap = open_stream(path)
        caps.append(cap)
    for i in range(n):
        name = "Display:"+str(i)
        window = open_window(name,x_offset(i),y_offset(i),full_screen)
        windows.append(window)
    INITIALISED = True

def video_playback(paths,fps,full_screen):
    video_setup(paths,full_screen)
    try:
        RUNNING = True
        while RUNNING:
            x = current_offset()
            for i in range(n):
                cap = caps[(x + i) % len(caps)]
                window = windows[i]
                RUNNING , frame = cap.read()
                if RUNNING:
                    cv2.imshow(window,frame)
                    if cv2.getWindowProperty(window,cv2.WND_PROP_VISIBLE) < 1:
                        RUNNING = False

            if n < len(caps):
                diff = len(caps) - n
                y = x + n
                for d in range(diff):
                    cap = caps[(y + d) % len(caps)]
                    RUNNING = cap.grab()

            key = cv2.waitKey(fps) & 0xff
            if key == QUIT_KEY:
                RUNNING = False
            elif key == NEXT_KEY:
                increment_offset()

    finally:
        for cap in caps:
            cap.release()
        for window in windows:
            cv2.destroyWindow(window)
