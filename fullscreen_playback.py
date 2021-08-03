
# IMPORTS
import cv2

# VARIABLES
full_screen = True
quit_key = ord('q')

# CHOICES
file = 'munching-squares_1920x1080.mp4'
first_camera = 0		# ... or webcam
second_camera = 1		# ... or webcam
choice = file

# OPEN THE CHOSEN VIDEO CAPTURE METHOD
cap = cv2.VideoCapture(choice)	# file / first_camera / second_camera
if(cap.isOpened() == False):
        print('Cannot open',str(choice))
        import sys
        sys.exit()

# ESTABLISH THE CORRECT FPS
if(choice == file):
        fps = round(cap.get(cv2.CAP_PROP_FPS))
else:
	fps = 1

# NAME THE NAMED WINDOW
video_window = str(choice)

# CONFIGURE THE NAMED WINDOW
if full_screen:
        cv2.namedWindow(video_window,cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(video_window,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
else:
        cv2.namedWindow(video_window,cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(video_window,0,0)

# MAIN LOOP
while(cap.isOpened()):
	ret , frame = cap.read()
	if ret == True:
		cv2.imshow(video_window,frame)
                # QUIT_KEY PRESSED ?
		if cv2.waitKey(fps) & 0xff == quit_key:
			break
                # WINDOW CLOSED ?
		if cv2.getWindowProperty(video_window,cv2.WND_PROP_VISIBLE) < 1:
			break
	else:
		break

# CLEAN UP
cap.release()
cv2.destroyWindow(video_window)
