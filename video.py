
import cv2

from display import n_displays , x_offset , y_offset

QUIT_KEY = ord('q')

def setup_window(file_path,window_name,x_offset,y_offset,full_screen):
    cap = cv2.VideoCapture(file_path)
    if(cap.isOpened() == False):
        print('Cannot open',file_path)
        return None , None
    video_window = window_name
    if full_screen:
        cv2.namedWindow(video_window,cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(video_window,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(video_window,cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(video_window,x_offset,y_offset)
    return cap , video_window

def video_playback(paths,fps,full_screen):
    caps = []
    windows = []
    n = n_displays()
    for i in range(n):
        path = paths[i % len(paths)]
        name = "Display:"+str(i)
        cap , window = setup_window(path,name,x_offset(i),y_offset(i),full_screen)
        if(cap == None or window == None):
            print('Cannot open window',str(i))
            return
        caps.append(cap)
        windows.append(window)
    try:
        RUNNING = True
        while RUNNING:
            for i in range(n):
                cap = caps[i]
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
