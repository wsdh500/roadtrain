
import cv2

from display import n_displays , x_offset , y_offset

from sys import exit

QUIT_KEY = ord('q')

caps = []
windows = []
n = n_displays()

def open_stream(stream):
    cap = cv2.VideoCapture(stream)
    if(cap.isOpened() == False):
        print('Cannot open stream',stream)
        sys.exit()
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

def video_playback(paths,fps,full_screen):
    for path in paths:
        cap = open_stream(path)
        caps.append(cap)
    for i in range(n):
        name = "Display:"+str(i)
        window = open_window(name,x_offset(i),y_offset(i),full_screen)
        windows.append(window)
    try:
        RUNNING = True
        while RUNNING:
            for i in range(n):
                cap = caps[i % len(caps)]
                window = windows[i]
                ret , frame = cap.read()
                if ret == True:
                    cv2.imshow(window,frame)
                    if cv2.getWindowProperty(window,cv2.WND_PROP_VISIBLE) < 1:
                        RUNNING = False
                else:
                    RUNNING = False
            if cv2.waitKey(fps) & 0xff == QUIT_KEY:
                RUNNING = False
    finally:
        for cap in caps:
            cap.release()
        for window in windows:
            cv2.destroyWindow(window)
